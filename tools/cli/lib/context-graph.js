import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { writeFileAtomic, withLock } from '../../lib/fs-atomic.js';
import { assertId } from '../../lib/paths.js';

export const RELATIONS = ['input_to', 'derived_from', 'impacts', 'references'];
export const NODE_TYPES = ['artifact', 'decision', 'debate'];

export const graphPathFor = projectRoot => join(projectRoot, '_mdan/state/context-graph.json');

function hashFile(projectRoot, path) {
  if (!projectRoot || !path) return null;
  const full = join(projectRoot, path);
  return existsSync(full) ? createHash('sha256').update(readFileSync(full)).digest('hex') : null;
}

const mermaidLabel = s => String(s).replace(/"/g, '#quot;');

export class ContextGraph {
  constructor(data = null) {
    this.version = data?.version || '1.1.0';
    this.nodes = data?.nodes || {};
    this.edges = data?.edges || [];
  }

  // Adds or updates a node. With `projectRoot`, the artifact file hash is recorded for staleness checks.
  addNode({ id, type = 'artifact', path = '', created_by = {}, metadata = {} }, projectRoot = null) {
    assertId(id, 'node id');
    if (!NODE_TYPES.includes(type)) throw new Error(`Invalid node type '${type}' (expected ${NODE_TYPES.join(', ')})`);
    const now = new Date().toISOString();
    const previous = this.nodes[id];
    this.nodes[id] = {
      id,
      type,
      path,
      created_at: previous?.created_at || now,
      updated_at: now,
      created_by,
      metadata,
      hash: hashFile(projectRoot, path),
    };
    return this.nodes[id];
  }

  removeNode(id) {
    delete this.nodes[id];
    this.edges = this.edges.filter(e => e.source !== id && e.target !== id);
  }

  addEdge({ source, target, relation = 'references' }) {
    if (!source || !target) throw new Error('Source and target required');
    if (!this.nodes[source]) throw new Error(`Source node '${source}' not found`);
    if (!this.nodes[target]) throw new Error(`Target node '${target}' not found`);
    if (!RELATIONS.includes(relation)) throw new Error(`Invalid relation '${relation}' (expected ${RELATIONS.join(', ')})`);
    if (source === target || this.getDownstream(target).some(n => n.id === source)) {
      throw new Error(`Edge ${source} -> ${target} would create a cycle`);
    }

    if (this.edges.some(e => e.source === source && e.target === target && e.relation === relation)) return;
    this.edges.push({ source, target, relation, created_at: new Date().toISOString() });
  }

  getNode(id) {
    return this.nodes[id] || null;
  }

  #traverse(startId, next) {
    const seen = new Set([startId]);
    const result = [];
    const queue = [startId];
    while (queue.length) {
      const current = queue.shift();
      for (const id of next(current)) {
        if (seen.has(id) || !this.nodes[id]) continue;
        seen.add(id);
        result.push(this.nodes[id]);
        queue.push(id);
      }
    }
    return result;
  }

  getDownstream(nodeId) {
    return this.#traverse(nodeId, id => this.edges.filter(e => e.source === id).map(e => e.target));
  }

  getUpstream(nodeId) {
    return this.#traverse(nodeId, id => this.edges.filter(e => e.target === id).map(e => e.source));
  }

  getEdgesFor(nodeId) {
    return this.edges.filter(e => e.source === nodeId || e.target === nodeId);
  }

  // Nodes whose artifact changed on disk since registration, and every node downstream of them.
  getStale(projectRoot) {
    const changed = Object.values(this.nodes).filter(n => {
      if (!n.path || !n.hash) return false;
      return hashFile(projectRoot, n.path) !== n.hash;
    });
    const stale = new Map();
    for (const node of changed) {
      for (const d of this.getDownstream(node.id)) {
        if (!stale.has(d.id)) stale.set(d.id, { node: d, because: node.id });
      }
    }
    return { changed, stale: [...stale.values()] };
  }

  // Re-records the current hash of a node's artifact (after it has been reviewed/updated).
  touch(id, projectRoot) {
    const node = this.nodes[id];
    if (!node) throw new Error(`Node '${id}' not found`);
    node.hash = hashFile(projectRoot, node.path);
    node.updated_at = new Date().toISOString();
    return node;
  }

  toMermaid() {
    const lines = ['graph TD'];
    for (const [id, node] of Object.entries(this.nodes)) {
      const label = [id, node.type, node.path].filter(Boolean).map(mermaidLabel).join('<br/>');
      lines.push(`  ${id}["${label}"]`);
    }
    for (const edge of this.edges) {
      const arrow = edge.relation === 'references' ? '-.->' : '-->';
      lines.push(`  ${edge.source} ${arrow}|${edge.relation}| ${edge.target}`);
    }
    return lines.join('\n');
  }

  toHtml(title = 'MDAN Context Graph') {
    const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
    return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>${esc(title)}</title>
<style>body{font-family:system-ui,sans-serif;margin:24px;background:#fff;color:#111}@media(prefers-color-scheme:dark){body{background:#111;color:#eee}}</style>
</head><body><h1>${esc(title)}</h1>
<pre class="mermaid">${esc(this.toMermaid())}</pre>
<script type="module">import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';mermaid.initialize({startOnLoad:true,theme:matchMedia('(prefers-color-scheme: dark)').matches?'dark':'default'});</script>
</body></html>
`;
  }

  toJSON() {
    return { version: this.version, nodes: this.nodes, edges: this.edges };
  }

  static load(filePath) {
    if (!existsSync(filePath)) return new ContextGraph();
    const raw = readFileSync(filePath, 'utf-8');
    try {
      return new ContextGraph(JSON.parse(raw));
    } catch (err) {
      throw new Error(`Corrupted context graph ${filePath}: ${err.message}`);
    }
  }

  save(filePath) {
    writeFileAtomic(filePath, JSON.stringify(this.toJSON(), null, 2) + '\n');
  }

  // Load-modify-save under a cross-process lock, so concurrent tool calls cannot lose writes.
  static update(filePath, fn) {
    return withLock(filePath, () => {
      const graph = ContextGraph.load(filePath);
      const result = fn(graph);
      graph.save(filePath);
      return result;
    });
  }
}
