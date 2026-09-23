import { z } from 'zod';
import { remember, recall, forget, endSession, listSidecars, MEMORY_TYPES } from '../../lib/memory.js';
import { safe, text } from '../util.js';

export function registerMemoryTools(server, projectRoot) {
  // Agent names are validated as safe ids by the memory library (party personas are allowed too).

  server.registerTool('mdan_memory_remember', {
    description: "Store a memory in an agent's persistent sidecar (observation, preference, project context or decision). Identical memories are reinforced, not duplicated",
    inputSchema: {
      agent: z.string().describe('Agent name (persona id, e.g. architect, risk-manager)'),
      content: z.string().min(1).max(500),
      type: z.enum(MEMORY_TYPES).default('observation'),
      confidence: z.number().min(0).max(1).default(0.6).describe('1.0 explicit decision/fact, 0.8 unchallenged argument, 0.6 observation, 0.5 inference'),
      tags: z.array(z.string()).optional(),
    },
  }, safe(async ({ agent, content, type, confidence, tags = [] }) => {
    const { memory, reinforced } = remember(projectRoot, agent, { content, type, confidence, tags });
    return text(`${reinforced ? 'Reinforced' : 'Stored'} memory ${memory.id} for ${agent} (confidence ${memory.confidence}).`);
  }));

  server.registerTool('mdan_memory_recall', {
    description: "Recall an agent's memories from previous sessions, highest confidence first",
    inputSchema: {
      agent: z.string(),
      query: z.string().optional().describe('Keywords to filter on (content and tags)'),
      type: z.enum(MEMORY_TYPES).optional(),
      limit: z.number().int().min(1).max(50).default(10),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ agent, query, type, limit }) => {
    const { sidecar, memories } = recall(projectRoot, agent, { query, type, limit });
    return text(JSON.stringify({
      agent,
      sessions: sidecar.sessions_participated,
      relationships: sidecar.relationships,
      decisions: sidecar.decision_history,
      memories,
    }, null, 2));
  }));

  server.registerTool('mdan_memory_forget', {
    description: 'Delete one memory from an agent sidecar',
    inputSchema: { agent: z.string(), id: z.string().describe('Memory id from mdan_memory_recall') },
    annotations: { destructiveHint: true },
  }, safe(async ({ agent, id }) => {
    forget(projectRoot, agent, id);
    return text(`Memory ${id} deleted for ${agent}.`);
  }));

  server.registerTool('mdan_memory_end_session', {
    description: 'Close a session for the participating agents: count the session, apply memory decay, record relationships and decision outcomes',
    inputSchema: {
      agents: z.array(z.object({
        name: z.string(),
        agrees_with: z.array(z.string()).optional(),
        disagrees_with: z.array(z.string()).optional(),
        complements: z.array(z.string()).optional(),
        decisions: z.array(z.object({
          dr_id: z.string(),
          role: z.enum(['proponent', 'opponent', 'arbitrator', 'participant']),
          position: z.string(),
          outcome: z.enum(['won', 'lost', 'compromised']),
        })).optional(),
      })).min(1),
    },
  }, safe(async ({ agents }) => {
    const lines = agents.map(a => {
      const s = endSession(projectRoot, a.name, {
        relationships: { agrees_with: a.agrees_with, disagrees_with: a.disagrees_with, complements: a.complements },
        decisions: a.decisions,
      });
      return `- ${a.name}: session ${s.sessions_participated}, ${s.memories.length} memories`;
    });
    return text(`Session closed:\n${lines.join('\n')}`);
  }));

  server.registerTool('mdan_memory_list', {
    description: 'List agents that have a memory sidecar',
    annotations: { readOnlyHint: true },
  }, safe(async () => text(JSON.stringify(listSidecars(projectRoot)))));
}
