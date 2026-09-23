// Agent memory sidecars (_mdan/state/sidecars/<agent>.sidecar.json), following the schema of
// _mdan/mdan/workflows/special/party-mode/templates/agent-sidecar.md.
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { writeFileAtomic, withLock } from './fs-atomic.js';
import { assertId, safeJoin } from './paths.js';

export const MEMORY_TYPES = ['observation', 'preference', 'context', 'decision'];
export const MAX_MEMORIES = 50;
// Memory decay: a memory not reinforced for this many sessions loses confidence.
export const DECAY_AFTER_SESSIONS = 5;
const DECAY_STEP = 0.1;
const MIN_CONFIDENCE = 0.3;

const sidecarDir = projectRoot => join(projectRoot, '_mdan/state/sidecars');
export const sidecarPath = (projectRoot, agent) =>
  safeJoin(sidecarDir(projectRoot), `${assertId(agent, 'agent name')}.sidecar.json`);

function emptySidecar(agent, displayName = agent) {
  const now = new Date().toISOString();
  return {
    agent,
    displayName,
    created_at: now,
    last_updated: now,
    sessions_participated: 0,
    memories: [],
    relationships: { agrees_with: [], disagrees_with: [], complements: [] },
    decision_history: [],
  };
}

export function loadSidecar(projectRoot, agent) {
  const file = sidecarPath(projectRoot, agent);
  if (!existsSync(file)) return emptySidecar(agent);
  return { ...emptySidecar(agent), ...JSON.parse(readFileSync(file, 'utf-8')) };
}

function updateSidecar(projectRoot, agent, fn) {
  const file = sidecarPath(projectRoot, agent);
  return withLock(file, () => {
    const sidecar = loadSidecar(projectRoot, agent);
    const result = fn(sidecar);
    sidecar.last_updated = new Date().toISOString();
    writeFileAtomic(file, JSON.stringify(sidecar, null, 2) + '\n');
    return result;
  });
}

function prune(sidecar) {
  if (sidecar.memories.length <= MAX_MEMORIES) return;
  sidecar.memories.sort((a, b) => b.confidence - a.confidence || b.created_at.localeCompare(a.created_at));
  sidecar.memories = sidecar.memories.slice(0, MAX_MEMORIES);
}

const normalize = s => s.toLowerCase().replace(/\s+/g, ' ').trim();

// Adds a memory; an identical memory is reinforced (confidence up, session reset) instead of duplicated.
export function remember(projectRoot, agent, { type = 'observation', content, confidence = 0.6, tags = [] }) {
  if (!MEMORY_TYPES.includes(type)) throw new Error(`Invalid memory type '${type}' (expected ${MEMORY_TYPES.join(', ')})`);
  if (!content?.trim()) throw new Error('Memory content is required');
  return updateSidecar(projectRoot, agent, s => {
    const existing = s.memories.find(m => normalize(m.content) === normalize(content));
    if (existing) {
      existing.confidence = Math.min(1, Math.max(existing.confidence, confidence) + 0.1);
      existing.last_reinforced_session = s.sessions_participated;
      existing.tags = [...new Set([...(existing.tags || []), ...tags])];
      return { memory: existing, reinforced: true };
    }
    const memory = {
      id: randomUUID().slice(0, 8),
      type,
      content: content.trim().slice(0, 500),
      confidence: Math.min(1, Math.max(0, confidence)),
      tags,
      source_session: new Date().toISOString(),
      created_at: new Date().toISOString(),
      last_reinforced_session: s.sessions_participated,
    };
    s.memories.push(memory);
    prune(s);
    return { memory, reinforced: false };
  });
}

// Relevant memories, highest confidence first; `query` matches content and tags (all terms).
export function recall(projectRoot, agent, { query = '', type, limit = 10 } = {}) {
  const s = loadSidecar(projectRoot, agent);
  const terms = normalize(query).split(' ').filter(Boolean);
  const memories = s.memories
    .filter(m => !type || m.type === type)
    .filter(m => terms.every(t => normalize(`${m.content} ${(m.tags || []).join(' ')}`).includes(t)))
    .sort((a, b) => b.confidence - a.confidence)
    .slice(0, limit);
  return { sidecar: s, memories };
}

export function forget(projectRoot, agent, id) {
  return updateSidecar(projectRoot, agent, s => {
    const before = s.memories.length;
    s.memories = s.memories.filter(m => m.id !== id);
    if (s.memories.length === before) throw new Error(`Memory '${id}' not found for agent '${agent}'`);
    return true;
  });
}

// Called once per session an agent takes part in: counts the session and decays stale memories.
export function endSession(projectRoot, agent, { relationships = {}, decisions = [] } = {}) {
  return updateSidecar(projectRoot, agent, s => {
    s.sessions_participated += 1;
    for (const m of s.memories) {
      const idle = s.sessions_participated - (m.last_reinforced_session ?? 0);
      if (idle > DECAY_AFTER_SESSIONS) m.confidence = Math.round(Math.max(0, m.confidence - DECAY_STEP) * 100) / 100;
    }
    s.memories = s.memories.filter(m => m.confidence >= MIN_CONFIDENCE);
    for (const key of ['agrees_with', 'disagrees_with', 'complements']) {
      s.relationships[key] = [...new Set([...(s.relationships[key] || []), ...(relationships[key] || [])])];
    }
    for (const d of decisions) {
      s.decision_history = s.decision_history.filter(x => x.dr_id !== d.dr_id);
      s.decision_history.push(d);
    }
    return s;
  });
}

export function listSidecars(projectRoot) {
  const dir = sidecarDir(projectRoot);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter(f => f.endsWith('.sidecar.json')).map(f => f.replace(/\.sidecar\.json$/, ''));
}

// Text block injected into an agent's context when it is loaded.
export function memoryBriefing(projectRoot, agent, limit = 10) {
  const { sidecar, memories } = recall(projectRoot, agent, { limit });
  if (!memories.length) return '';
  const lines = memories.map(m => `- [${m.type}] ${m.content} (confidence: ${m.confidence})`);
  const rel = Object.entries(sidecar.relationships).filter(([, v]) => v.length).map(([k, v]) => `${k}: ${v.join(', ')}`);
  return `## 📝 Memories from previous sessions (${sidecar.sessions_participated} sessions)\n\n${lines.join('\n')}` +
    (rel.length ? `\n\n🤝 ${rel.join(' · ')}` : '');
}
