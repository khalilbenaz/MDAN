import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { loadState, updateState, startWorkflow, setStep, completeWorkflow, nextStep, summarize } from '../tools/lib/state.js';
import { remember, recall, forget, endSession, memoryBriefing, MAX_MEMORIES, DECAY_AFTER_SESSIONS } from '../tools/lib/memory.js';

const tmp = () => mkdtempSync(join(tmpdir(), 'mdan-state-'));

test('state: start, step, complete and next step follow the method order', () => {
  const root = tmp();
  assert.equal(nextStep(loadState(root)).workflow, 'create-product-brief');

  updateState(root, s => startWorkflow(s, 'create-product-brief'));
  updateState(root, s => setStep(s, 'create-product-brief', 'step-03-users', 'steps/step-03-users.md'));
  let s = loadState(root);
  assert.deepEqual(nextStep(s), { workflow: 'create-product-brief', reason: 'resume', step: 'step-03-users' });

  updateState(root, st => completeWorkflow(st, 'create-product-brief', { artifacts: [{ id: 'brief', path: 'docs/brief.md' }] }));
  s = loadState(root);
  assert.equal(s.current_workflow, null);
  assert.equal(s.artifacts[0].id, 'brief');
  assert.equal(nextStep(s).workflow, 'create-prd');
});

test('state: restarting the same workflow keeps its resume point', () => {
  const root = tmp();
  updateState(root, s => setStep(s, 'create-prd', 'step-07'));
  updateState(root, s => startWorkflow(s, 'create-prd'));
  assert.equal(loadState(root).current_workflow.step, 'step-07');
});

test('state: next step skips workflows that are not installed', () => {
  const root = tmp();
  updateState(root, s => completeWorkflow(s, 'create-product-brief'));
  assert.equal(nextStep(loadState(root), ['create-product-brief', 'create-architecture']).workflow, 'create-architecture');
  assert.ok(summarize(loadState(root)).phases.length >= 5);
});

test('memory: remember, reinforce, recall, forget', () => {
  const root = tmp();
  const a = remember(root, 'architect', { content: 'Prefers modular monolith', type: 'preference', confidence: 0.6, tags: ['archi'] });
  assert.equal(a.reinforced, false);
  const b = remember(root, 'architect', { content: 'prefers  modular MONOLITH', confidence: 0.6 });
  assert.equal(b.reinforced, true);
  assert.equal(b.memory.confidence, 0.7);

  remember(root, 'architect', { content: 'PostgreSQL chosen for ACID', type: 'decision', confidence: 1 });
  const { memories } = recall(root, 'architect');
  assert.equal(memories[0].content, 'PostgreSQL chosen for ACID');
  assert.equal(recall(root, 'architect', { query: 'archi' }).memories.length, 1);
  assert.match(memoryBriefing(root, 'architect'), /\[decision\] PostgreSQL/);

  forget(root, 'architect', a.memory.id);
  assert.equal(recall(root, 'architect').memories.length, 1);
  assert.throws(() => forget(root, 'architect', 'nope'), /not found/);
});

test('memory: capped, decays when not reinforced, records relationships', () => {
  const root = tmp();
  for (let i = 0; i < MAX_MEMORIES + 10; i++) remember(root, 'pm', { content: `fact ${i}`, confidence: i % 2 ? 0.9 : 0.5 });
  assert.equal(recall(root, 'pm', { limit: 100 }).memories.length, MAX_MEMORIES);

  const root2 = tmp();
  remember(root2, 'dev', { content: 'uses pnpm', confidence: 0.5 });
  for (let i = 0; i < DECAY_AFTER_SESSIONS + 3; i++) endSession(root2, 'dev', { relationships: { agrees_with: ['architect'] } });
  const { sidecar, memories } = recall(root2, 'dev');
  assert.equal(memories.length, 0, 'low-confidence memory decayed away');
  assert.deepEqual(sidecar.relationships.agrees_with, ['architect']);
  assert.equal(sidecar.sessions_participated, DECAY_AFTER_SESSIONS + 3);
});

test('memory: agent names cannot escape the sidecar directory', () => {
  assert.throws(() => remember(tmp(), '../evil', { content: 'x' }), /Invalid agent name/);
});
