import { readFile } from 'node:fs/promises';
import { existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { z } from 'zod';
import { ContextGraph, graphPathFor } from '../../cli/lib/context-graph.js';
import { assertId, safeJoin } from '../../lib/paths.js';
import { writeFileAtomic, withLock } from '../../lib/fs-atomic.js';
import { safe, text } from '../util.js';
import { updateState, recordDecision } from '../../lib/state.js';
import { memoryBriefing } from '../../lib/memory.js';

const PARTY = '_mdan/mdan/workflows/special/party-mode';
const MODE_STEPS = { debate: 'steps/step-02a-debate-mode.md', consensus: 'steps/step-02b-consensus-mode.md' };

function nextDecisionId(dir) {
  if (!existsSync(dir)) return 'DR-001';
  const numbers = readdirSync(dir)
    .map(f => f.match(/^DR-(\d+)\.json$/)?.[1])
    .filter(Boolean)
    .map(Number);
  return `DR-${String((numbers.length ? Math.max(...numbers) : 0) + 1).padStart(3, '0')}`;
}

// contentRoot: where the _mdan content lives; projectRoot: where decisions and the graph are written.
export function registerOrchestrationTools(server, discovery, projectRoot, contentRoot = projectRoot) {
  const agentNames = new Set(discovery.agents.map(a => a.name));

  server.registerTool('mdan_party_mode', {
    description: 'Start a multi-agent session: free discussion, structured debate (-> decision record) or consensus',
    inputSchema: {
      mode: z.enum(['discussion', 'debate', 'consensus']).default('discussion'),
      topic: z.string().optional().describe('Topic for the session'),
      agents: z.array(z.string()).optional().describe('Agent names to include (default: all installed)'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ mode, topic, agents }) => {
    const unknown = (agents || []).filter(a => !agentNames.has(a));
    if (unknown.length) throw new Error(`Unknown agent(s): ${unknown.join(', ')}`);
    const wizard = await readFile(safeJoin(contentRoot, PARTY, 'wizard.md'), 'utf-8');
    const stepPath = MODE_STEPS[mode] && safeJoin(contentRoot, PARTY, MODE_STEPS[mode]);
    const modeStep = stepPath && existsSync(stepPath) ? await readFile(stepPath, 'utf-8') : '';
    return text([
      '# Multi-Agent Orchestration', '',
      `**Mode:** ${mode}`,
      `**Topic:** ${topic || '(ask the user)'}`,
      `**Agents:** ${agents?.length ? agents.join(', ') : 'all installed'}`,
      '', '---', '', wizard,
      modeStep ? `\n---\n\n## Mode-Specific Protocol\n\n${modeStep}` : '',
      ...(agents || []).map(a => [a, memoryBriefing(projectRoot, a)]).filter(([, b]) => b).map(([a, b]) => `\n### ${a}\n${b}`),
      '\n---\n\nOn exit: store new memories with `mdan_memory_remember`, then call `mdan_memory_end_session` for every participant.',
      mode === 'debate' || mode === 'consensus'
        ? '\n---\n\nAt the end, call `mdan_create_decision_record` with the outcome (and `impacts` = artifact node ids affected).'
        : '',
    ].join('\n'));
  }));

  server.registerTool('mdan_create_decision_record', {
    description: 'Save a decision record (DR-XXX) from a debate or consensus session and register it in the context graph',
    inputSchema: {
      id: z.string().optional().describe('Decision record ID (default: next DR-XXX)'),
      topic: z.string().describe('Decision topic'),
      mode: z.enum(['debate', 'consensus']).default('debate'),
      decision: z.string().describe('Final decision'),
      rationale: z.string().describe('Rationale for the decision'),
      confidence: z.number().min(0).max(1).default(0.5).describe('Confidence score 0-1'),
      participants: z.record(z.string(), z.any()).optional().describe('Participants, e.g. {"partisan":"winston","opposant":"amelia"}'),
      rounds: z.array(z.any()).optional().describe('Debate rounds'),
      dissent: z.string().optional().describe('Dissenting opinion, if any'),
      impacts: z.array(z.string()).optional().describe('Context graph node ids impacted by this decision'),
    },
  }, safe(async ({ id, topic, mode, decision, rationale, confidence, participants, rounds, dissent, impacts }) => {
    const dir = join(projectRoot, 'mdan_output', 'decisions');
    // withLock is synchronous: id allocation + write happen atomically across processes.
    const record = withLock(join(dir, '.decisions'), () => {
      const recordId = id ? assertId(id, 'decision id') : nextDecisionId(dir);
      const r = {
        id: recordId, topic, mode, participants: participants || {}, rounds: rounds || [],
        decision, rationale, confidence, dissent: dissent || null,
        date: new Date().toISOString(), registered_in_graph: true,
      };
      writeFileAtomic(safeJoin(dir, `${recordId}.json`), JSON.stringify(r, null, 2) + '\n');
      return r;
    });

    const relPath = `mdan_output/decisions/${record.id}.json`;
    const missing = [];
    ContextGraph.update(graphPathFor(projectRoot), g => {
      g.addNode({ id: record.id, type: 'decision', path: relPath, metadata: { topic, mode, confidence } }, projectRoot);
      for (const target of impacts || []) {
        if (g.getNode(target)) g.addEdge({ source: record.id, target, relation: 'impacts' });
        else missing.push(target);
      }
    });

    updateState(projectRoot, state => recordDecision(state, { id: record.id, topic, decision }));

    return text(`Decision record ${record.id} saved to ${relPath} and registered in the context graph.` +
      (missing.length ? `\nWarning: unknown impacted node(s) skipped: ${missing.join(', ')}` : ''));
  }));
}
