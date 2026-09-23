import { z } from 'zod';
import { loadState, updateState, startWorkflow, setStep, completeWorkflow, summarize } from '../../lib/state.js';
import { ContextGraph, graphPathFor } from '../../cli/lib/context-graph.js';
import { safeJoin } from '../../lib/paths.js';
import { safe, text } from '../util.js';

export function registerStateTools(server, discovery, projectRoot) {
  const installed = discovery.workflows.map(w => w.name);

  server.registerTool('mdan_status', {
    description: 'Project status: current workflow and step, completed workflows per phase, artifacts, decisions and the recommended next step',
    annotations: { readOnlyHint: true },
  }, safe(async () => {
    const s = summarize(loadState(projectRoot), installed);
    const stale = ContextGraph.load(graphPathFor(projectRoot)).getStale(projectRoot).stale;
    return text(JSON.stringify({ ...s, staleArtifacts: stale.map(x => ({ id: x.node.id, because: x.because })) }, null, 2));
  }));

  server.registerTool('mdan_state_update', {
    description: 'Record workflow progress: "start" (or resume) a workflow, "step" when moving to a step, "complete" with the produced artifacts (also registered in the context graph)',
    inputSchema: {
      action: z.enum(['start', 'step', 'complete']),
      workflow: z.string().describe('Workflow name'),
      step: z.string().optional().describe('Current step id, e.g. "step-07-project-type"'),
      stepFile: z.string().optional().describe('Path of the current step file'),
      artifacts: z.array(z.object({
        id: z.string().describe('Graph node id, e.g. prd'),
        path: z.string().describe('Artifact path relative to the project root'),
        inputs: z.array(z.string()).optional().describe('Node ids this artifact was built from'),
      })).optional(),
      summary: z.string().optional().describe('Updated project context summary'),
    },
  }, safe(async ({ action, workflow, step, stepFile, artifacts = [], summary }) => {
    if (installed.length && !installed.includes(workflow)) throw new Error(`Unknown workflow '${workflow}'`);
    for (const a of artifacts) safeJoin(projectRoot, a.path);

    const result = updateState(projectRoot, state => {
      if (action === 'start') return startWorkflow(state, workflow, { step, stepFile });
      if (action === 'step') {
        if (!step) throw new Error('"step" is required for action "step"');
        return setStep(state, workflow, step, stepFile);
      }
      completeWorkflow(state, workflow, { artifacts: artifacts.map(({ id, path }) => ({ id, path })), summary });
      return null;
    });

    const missing = [];
    if (action === 'complete' && artifacts.length) {
      ContextGraph.update(graphPathFor(projectRoot), g => {
        for (const a of artifacts) g.addNode({ id: a.id, path: a.path, created_by: { workflow } }, projectRoot);
        for (const a of artifacts) {
          for (const input of a.inputs || []) {
            if (g.getNode(input)) g.addEdge({ source: input, target: a.id, relation: 'input_to' });
            else missing.push(input);
          }
        }
      });
    }
    const next = summarize(loadState(projectRoot), installed).next;
    return text([
      action === 'complete' ? `Workflow '${workflow}' completed${artifacts.length ? ` — ${artifacts.length} artifact(s) registered in the context graph` : ''}.`
        : `Workflow '${workflow}' ${action === 'start' ? 'started' : 'at step'} ${result?.step || ''}`.trim() + '.',
      missing.length ? `Warning: unknown input node(s) skipped: ${missing.join(', ')}` : '',
      action === 'complete' && next ? `Next recommended: ${next.workflow}` : '',
    ].filter(Boolean).join('\n'));
  }));
}
