import { z } from 'zod';
import { exportBacklog, buildBacklog, toCsvExport } from '../../lib/export.js';
import { safeJoin } from '../../lib/paths.js';
import { safe, text } from '../util.js';

export function registerExportTools(server, projectRoot) {
  server.registerTool('mdan_export_backlog', {
    description: 'Export the epics/stories document to CSV, GitHub Issues, Azure DevOps Boards or Jira. Dry run by default (returns the planned requests); apply=true sends them (tokens from environment variables). Re-runs update instead of duplicating',
    inputSchema: {
      target: z.enum(['csv', 'github', 'ado', 'jira']),
      apply: z.boolean().default(false),
      file: z.string().optional().describe('Epics document path (default: from the project state)'),
      repo: z.string().optional().describe('github: owner/name'),
      org: z.string().optional().describe('ado: organization'),
      project: z.string().optional().describe('ado project name or jira project key'),
      url: z.string().optional().describe('jira: https://<site>.atlassian.net'),
    },
    annotations: { openWorldHint: true },
  }, safe(async ({ target, apply, file, ...options }) => {
    if (file) safeJoin(projectRoot, file);
    if (target === 'csv') return text(toCsvExport(buildBacklog(projectRoot, file)));
    const r = await exportBacklog(projectRoot, target, { apply, file, options });
    return text(JSON.stringify({ ...r, operations: r.operations.map(({ key, method, url }) => ({ key, method, url })) }, null, 2));
  }));
}
