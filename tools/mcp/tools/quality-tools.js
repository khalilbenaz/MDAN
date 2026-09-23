import { z } from 'zod';
import { checkProject, traceability, registerTrace, detectScale, SCALES } from '../../lib/quality.js';
import { estimateScope } from '../../lib/scope.js';
import { ContextGraph, graphPathFor } from '../../cli/lib/context-graph.js';
import { safeJoin } from '../../lib/paths.js';
import { safe, text } from '../util.js';

export function registerQualityTools(server, projectRoot) {
  server.registerTool('mdan_check', {
    description: 'Quality gate on the project artifacts (brief, PRD, architecture, epics, tech spec): unfilled placeholders, empty sections, missing sections, FR/NFR coverage across documents, acceptance criteria. Strictness follows the project scale',
    inputSchema: {
      paths: z.array(z.string()).optional().describe('Artifacts to check (default: those registered in the state, then docs/)'),
      scale: z.enum(SCALES).optional().describe('Override the detected scale'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ paths, scale }) => {
    for (const p of paths || []) safeJoin(projectRoot, p);
    return text(JSON.stringify(checkProject(projectRoot, { paths, scale: scale || detectScale(projectRoot).scale }), null, 2));
  }));

  server.registerTool('mdan_trace', {
    description: 'Traceability matrix requirement (FR/NFR) → stories → tests, coverage and gate decision; optionally writes it into the context graph',
    inputSchema: { register: z.boolean().default(false).describe('Also add requirement/story/test nodes and edges to the context graph') },
  }, safe(async ({ register }) => {
    const trace = traceability(projectRoot);
    const added = register ? registerTrace(projectRoot, trace, ContextGraph, graphPathFor(projectRoot)) : 0;
    return text(JSON.stringify({ ...trace, graphNodesAdded: added }, null, 2));
  }));

  server.registerTool('mdan_estimate_scope', {
    description: 'Decide how much process a change needs (oneshot quick-dev / quick-spec first / full planning) from its description, files and the real downstream impact in the context graph',
    inputSchema: {
      description: z.string().min(1),
      files: z.array(z.string()).optional(),
      artifacts: z.array(z.string()).optional().describe('Context graph node ids touched by the change'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async args => text(JSON.stringify(estimateScope(projectRoot, args), null, 2))));
}
