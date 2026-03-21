import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export function registerStateResource(server, projectRoot) {
  server.resource(
    'mdan://state',
    'mdan://state',
    async () => {
      const statePath = join(projectRoot, '_mdan/state/MDAN-STATE.json');
      let content = '{}';
      if (existsSync(statePath)) {
        content = await readFile(statePath, 'utf-8');
      }
      return {
        contents: [{
          uri: 'mdan://state',
          mimeType: 'application/json',
          text: content,
        }],
      };
    }
  );
}
