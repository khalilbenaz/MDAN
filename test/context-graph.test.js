import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { ContextGraph } from '../tools/cli/lib/context-graph.js';

const tmp = () => mkdtempSync(join(tmpdir(), 'mdan-graph-'));

function chain() {
  const g = new ContextGraph();
  for (const id of ['prd', 'arch', 'epics', 'sprint']) g.addNode({ id });
  g.addEdge({ source: 'prd', target: 'arch', relation: 'input_to' });
  g.addEdge({ source: 'arch', target: 'epics', relation: 'input_to' });
  g.addEdge({ source: 'epics', target: 'sprint', relation: 'input_to' });
  return g;
}

test('downstream and upstream are transitive and deduplicated', () => {
  const g = chain();
  g.addNode({ id: 'ux' });
  g.addEdge({ source: 'prd', target: 'ux', relation: 'input_to' });
  g.addEdge({ source: 'ux', target: 'epics', relation: 'input_to' });
  assert.deepEqual(g.getDownstream('prd').map(n => n.id).sort(), ['arch', 'epics', 'sprint', 'ux']);
  assert.deepEqual(g.getUpstream('sprint').map(n => n.id).sort(), ['arch', 'epics', 'prd', 'ux']);
});

test('cycles, self-loops, unknown nodes and relations are rejected', () => {
  const g = chain();
  assert.throws(() => g.addEdge({ source: 'sprint', target: 'prd' }), /cycle/);
  assert.throws(() => g.addEdge({ source: 'prd', target: 'prd' }), /cycle/);
  assert.throws(() => g.addEdge({ source: 'prd', target: 'nope' }), /not found/);
  assert.throws(() => g.addEdge({ source: 'prd', target: 'sprint', relation: 'likes' }), /Invalid relation/);
});

test('node ids cannot contain path separators', () => {
  assert.throws(() => new ContextGraph().addNode({ id: '../x' }), /Invalid node id/);
});

test('duplicate edges are ignored', () => {
  const g = chain();
  g.addEdge({ source: 'prd', target: 'arch', relation: 'input_to' });
  assert.equal(g.edges.length, 3);
});

test('stale detection follows file hashes downstream', () => {
  const root = tmp();
  mkdirSync(join(root, 'docs'));
  writeFileSync(join(root, 'docs/prd.md'), 'v1');
  const g = new ContextGraph();
  g.addNode({ id: 'prd', path: 'docs/prd.md' }, root);
  g.addNode({ id: 'arch' }, root);
  g.addEdge({ source: 'prd', target: 'arch', relation: 'input_to' });
  assert.equal(g.getStale(root).changed.length, 0);

  writeFileSync(join(root, 'docs/prd.md'), 'v2');
  const { changed, stale } = g.getStale(root);
  assert.deepEqual(changed.map(n => n.id), ['prd']);
  assert.deepEqual(stale.map(s => s.node.id), ['arch']);

  g.touch('prd', root);
  assert.equal(g.getStale(root).changed.length, 0);
});

test('update() persists atomically and survives reload', () => {
  const file = join(tmp(), 'state', 'graph.json');
  ContextGraph.update(file, g => g.addNode({ id: 'a' }));
  ContextGraph.update(file, g => { g.addNode({ id: 'b' }); g.addEdge({ source: 'a', target: 'b', relation: 'impacts' }); });
  const g = ContextGraph.load(file);
  assert.deepEqual(Object.keys(g.nodes), ['a', 'b']);
  assert.match(g.toMermaid(), /a -->\|impacts\| b/);
  assert.match(g.toHtml(), /class="mermaid"/);
});
