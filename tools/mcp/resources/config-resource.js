import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export function registerConfigResource(server, discovery, projectRoot) {
  server.resource(
    'mdan://config',
    'mdan://config',
    async () => {
      const configs = {};

      // Load each module's config
      for (const mod of discovery.modules) {
        const configPath = join(projectRoot, `_mdan/${mod}/config.yaml`);
        if (existsSync(configPath)) {
          configs[mod] = await readFile(configPath, 'utf-8');
        }
      }

      return {
        contents: [{
          uri: 'mdan://config',
          mimeType: 'application/json',
          text: JSON.stringify({
            manifest: discovery.manifest,
            modules: discovery.modules,
            configs,
            workflowCount: discovery.workflows.length,
            agentCount: discovery.agents.length,
          }, null, 2),
        }],
      };
    }
  );
}
