import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname } from 'node:path';

export class ContextGraph {
  constructor(data = null) {
    this.version = '1.0.0';
    this.nodes = {};
    this.edges = [];
    if (data) {
      this.version = data.version || '1.0.0';
      this.nodes = data.nodes || {};
      this.edges = data.edges || [];
    }
  }

  addNode({ id, type = 'artifact', path = '', created_by = {}, metadata = {} }) {
    if (!id) throw new Error('Node ID required');
    this.nodes[id] = {
      id,
      type,
      path,
      created_at: new Date().toISOString(),
      created_by,
      metadata,
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

    const exists = this.edges.some(e => e.source === source && e.target === target && e.relation === relation);
    if (exists) return;

    this.edges.push({
      source,
      target,
      relation,
      created_at: new Date().toISOString(),
    });
  }

  getNode(id) {
    return this.nodes[id] || null;
  }

  getDownstream(nodeId, visited = new Set()) {
    if (visited.has(nodeId)) return [];
    visited.add(nodeId);

    const directTargets = this.edges
      .filter(e => e.source === nodeId)
      .map(e => e.target);

    const result = [];
    for (const targetId of directTargets) {
      const node = this.nodes[targetId];
      if (node) {
        result.push(node);
        result.push(...this.getDownstream(targetId, visited));
      }
    }
    return result;
  }

  getUpstream(nodeId, visited = new Set()) {
    if (visited.has(nodeId)) return [];
    visited.add(nodeId);

    const directSources = this.edges
      .filter(e => e.target === nodeId)
      .map(e => e.source);

    const result = [];
    for (const sourceId of directSources) {
      const node = this.nodes[sourceId];
      if (node) {
        result.push(node);
        result.push(...this.getUpstream(sourceId, visited));
      }
    }
    return result;
  }

  getEdgesFor(nodeId) {
    return this.edges.filter(e => e.source === nodeId || e.target === nodeId);
  }

  toMermaid() {
    const lines = ['graph TD'];

    for (const [id, node] of Object.entries(this.nodes)) {
      const label = node.path ? `${id}[${id}\\n${node.type}\\n${node.path}]` : `${id}[${id}\\n${node.type}]`;
      lines.push(`  ${label}`);
    }

    const arrowMap = {
      input_to: '-->|input_to|',
      derived_from: '-->|derived_from|',
      impacts: '-->|impacts|',
      references: '-.->|references|',
    };

    for (const edge of this.edges) {
      const arrow = arrowMap[edge.relation] || '-->|' + edge.relation + '|';
      lines.push(`  ${edge.source} ${arrow} ${edge.target}`);
    }

    return lines.join('\n');
  }

  toJSON() {
    return {
      version: this.version,
      nodes: this.nodes,
      edges: this.edges,
    };
  }

  static load(filePath) {
    if (!existsSync(filePath)) {
      return new ContextGraph();
    }
    const raw = readFileSync(filePath, 'utf-8');
    return new ContextGraph(JSON.parse(raw));
  }

  save(filePath) {
    const dir = dirname(filePath);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    writeFileSync(filePath, JSON.stringify(this.toJSON(), null, 2));
  }
}
