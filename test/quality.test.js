import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { checkArtifact, checkProject, traceability, registerTrace, parseEpics, definedRequirements, detectScale } from '../tools/lib/quality.js';
import { estimateScope } from '../tools/lib/scope.js';
import { updateState, completeWorkflow } from '../tools/lib/state.js';
import { ContextGraph, graphPathFor } from '../tools/cli/lib/context-graph.js';

const PRD = `# Product Requirements Document - Wallet

## Functional Requirements
- FR1: A customer can open a level-1 wallet with a phone number
- FR2: A customer can send money to another wallet
- FR3: An agent can cash-in for a customer

## Non-Functional Requirements
- NFR1: P2P transfer p95 latency below 800 ms
- NFR2: The app must be fast
`;

const EPICS = `# Wallet - Epic Breakdown

## Epic 1: Onboarding

### Story 1.1: Open wallet
Covers FR1.

**Given** a new phone number **When** the customer signs up **Then** a level-1 wallet exists

## Epic 2: Transfers

### Story 2.1: P2P transfer
Implements FR2 within NFR1.

**Given** two wallets **When** A sends 100 MAD **Then** B is credited
`;

function project() {
  const root = mkdtempSync(join(tmpdir(), 'mdan-quality-'));
  mkdirSync(join(root, 'docs'));
  mkdirSync(join(root, 'test'));
  writeFileSync(join(root, 'docs/prd.md'), PRD);
  writeFileSync(join(root, 'docs/epics.md'), EPICS);
  writeFileSync(join(root, 'test/onboarding.test.js'), "// Story 1.1\ntest('opens a wallet (FR1)', () => {});");
  updateState(root, s => completeWorkflow(s, 'create-prd', { artifacts: [{ id: 'prd', path: 'docs/prd.md' }] }));
  updateState(root, s => completeWorkflow(s, 'create-epics-and-stories', { artifacts: [{ id: 'epics', path: 'docs/epics.md' }] }));
  return root;
}

test('parsing: requirements and epics/stories', () => {
  assert.deepEqual([...definedRequirements(PRD).keys()], ['FR1', 'FR2', 'FR3', 'NFR1', 'NFR2']);
  const epics = parseEpics(EPICS);
  assert.equal(epics.length, 2);
  assert.deepEqual(epics[1].stories[0].requirements, ['FR2', 'NFR1']);
  assert.ok(epics[0].stories[0].hasCriteria);
});

test('check: placeholders, empty sections and vague requirements are reported', () => {
  const r = checkArtifact('docs/prd.md', `${PRD}\n## Risks\n\n## Open questions\n{{question}}\n`, { scale: 'team' });
  const rules = r.issues.map(i => i.rule);
  assert.ok(rules.includes('placeholders'));
  assert.ok(rules.includes('empty-sections'));
  assert.ok(rules.includes('measurable'), 'NFR2 "fast" without a number');
  assert.equal(r.decision, 'FAIL');
});

test('check: epics must cover every PRD requirement; strictness follows the scale', () => {
  const root = project();
  const report = checkProject(root, { scale: 'team' });
  const epics = report.results.find(r => r.kind === 'epics');
  assert.match(epics.issues.find(i => i.rule === 'fr-coverage').message, /FR3/);
  assert.equal(report.decision, 'FAIL');

  const prdOnly = checkArtifact('docs/prd.md', PRD, { scale: 'solo' });
  assert.equal(prdOnly.decision, 'PASS', 'solo tolerates warnings');
  assert.equal(checkArtifact('docs/prd.md', PRD, { scale: 'enterprise' }).decision, 'FAIL');
});

test('scale is detected from the number of stories', () => {
  assert.equal(detectScale(project()).scale, 'solo');
});

test('traceability matrix links requirements, stories and tests, and lands in the graph', () => {
  const root = project();
  const t = traceability(root, { scale: 'team' });
  const fr1 = t.rows.find(r => r.id === 'FR1');
  assert.deepEqual(fr1.stories, ['1.1']);
  assert.deepEqual(fr1.tests, ['test/onboarding.test.js']);
  assert.deepEqual(t.rows.find(r => r.id === 'FR3').stories, []);
  assert.equal(t.decision, 'FAIL', 'FR3 has no story');
  assert.deepEqual(t.untestedStories, ['2.1']);

  const added = registerTrace(root, t, ContextGraph, graphPathFor(root));
  assert.ok(added >= 4);
  const g = ContextGraph.load(graphPathFor(root));
  assert.deepEqual(g.getDownstream('FR1').map(n => n.id).sort(), ['story-1.1', 'test-test-onboarding.test.js']);
});

test('scope routing: tiny change → oneshot, risky wide change → full', () => {
  const root = project();
  assert.equal(estimateScope(root, { description: 'fix typo in button label', files: ['src/Button.tsx'] }).route, 'oneshot');
  const big = estimateScope(root, {
    description: 'change the wallet ledger schema and payment authorization flow',
    files: Array.from({ length: 12 }, (_, i) => `src/f${i}.ts`),
    artifacts: ['prd'],
  });
  assert.equal(big.route, 'full');
  assert.ok(big.reasons.some(r => /money movement/.test(r)));
});
