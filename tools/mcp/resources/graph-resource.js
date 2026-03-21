import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export function registerGraphResource(server, projectRoot) {
  server.resource(
    'mdan://graph',
    'mdan://graph',
    async () => {
      const graphPath = join(projectRoot, '_mdan/state/context-graph.json');
      let content = JSON.stringify({ version: '1.0.0', nodes: {}, edges: [] });
      if (existsSync(graphPath)) {
        content = await readFile(graphPath, 'utf-8');
      }
      return {
        contents: [{
          uri: 'mdan://graph',
          mimeType: 'application/json',
          text: content,
        }],
      };
    }
  );
}
