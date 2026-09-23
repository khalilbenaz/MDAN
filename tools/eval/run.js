#!/usr/bin/env node
// Wizard evaluation harness: an LLM runs an MDAN wizard end to end while a second LLM plays the user
// from a scenario, then the produced document goes through the deterministic quality gate (mdan check).
// Catches regressions in the *content* (broken step chains, missing sections, lost requirements).
//
//   ANTHROPIC_API_KEY=... node tools/eval/run.js [scenario ...] [--model claude-sonnet-5] [--turns 30]
//
// Not part of CI (costs tokens); run before releasing content changes.
import { readFileSync, readdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, basename } from 'node:path';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';
import { readSources } from '../lib/sources.js';
import { renderWorkflow } from '../mcp/tools/workflow-tools.js';
import { checkArtifact } from '../lib/quality.js';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const SCENARIOS = join(ROOT, 'tools/eval/scenarios');
const DONE = '<<<MDAN_DOCUMENT>>>';

async function claude(model, system, messages, maxTokens = 4096) {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({ model, max_tokens: maxTokens, system, messages }),
  });
  if (!res.ok) throw new Error(`Anthropic API ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const json = await res.json();
  return json.content.filter(b => b.type === 'text').map(b => b.text).join('\n');
}

async function runScenario(file, { model, turns }) {
  const scenario = JSON.parse(readFileSync(file, 'utf-8'));
  const wf = readSources(ROOT).workflows.find(w => w.name === scenario.workflow);
  if (!wf) throw new Error(`Unknown workflow ${scenario.workflow}`);

  const system = `${await renderWorkflow(ROOT, wf, scenario.topic, ROOT)}

---
EVALUATION MODE: there are no tools and no file system. Load step files by quoting from memory of the sections above when they are included; when a step file is not included, follow its purpose from the wizard. Keep each message short. When the final document is complete, output the line ${DONE} followed by the whole document in markdown, and nothing after it.`;
  const userSystem = `You are role-playing the user of a product-planning assistant. Scenario:\n${scenario.persona}\n\nAnswer the assistant's questions concisely and consistently with the scenario. When it shows a menu, pick the option that moves forward (usually "C" / continue). Never write the document yourself.`;

  const transcript = [{ role: 'user', content: `Start the ${scenario.workflow} workflow. Topic: ${scenario.topic}` }];
  let document = null;
  for (let i = 0; i < turns && !document; i++) {
    const reply = await claude(model, system, transcript, 8000);
    transcript.push({ role: 'assistant', content: reply });
    if (reply.includes(DONE)) {
      document = reply.slice(reply.indexOf(DONE) + DONE.length).trim();
      break;
    }
    const flipped = transcript.map(m => ({ role: m.role === 'user' ? 'assistant' : 'user', content: m.content }));
    transcript.push({ role: 'user', content: await claude(model, userSystem, flipped.slice(1), 1024) });
  }

  const result = document
    ? checkArtifact(`${scenario.kind}.md`, document, { kind: scenario.kind, scale: scenario.scale || 'team' })
    : { decision: 'FAIL', score: 0, issues: [{ level: 'error', rule: 'no-document', message: `No document after ${turns} turns` }] };
  const expected = (scenario.expect?.requirements || []).filter(r => document && !new RegExp(`\\b${r}\\b`).test(document));
  if (expected.length) result.issues.push({ level: 'error', rule: 'expected-content', message: `Missing: ${expected.join(', ')}` });

  const outDir = join(ROOT, 'tools/eval/out');
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, `${basename(file, '.json')}.md`), document || '(no document)');
  writeFileSync(join(outDir, `${basename(file, '.json')}.transcript.json`), JSON.stringify(transcript, null, 2));
  const pass = document && result.decision !== 'FAIL' && !expected.length;
  return { scenario: basename(file, '.json'), turns: Math.ceil(transcript.length / 2), pass, ...result };
}

const { values, positionals } = parseArgs({
  allowPositionals: true,
  options: { model: { type: 'string', default: 'claude-sonnet-5' }, turns: { type: 'string', default: '30' } },
});
if (!process.env.ANTHROPIC_API_KEY) {
  console.error('Set ANTHROPIC_API_KEY to run the wizard evaluations.');
  process.exit(1);
}
const files = (positionals.length ? positionals : readdirSync(SCENARIOS).filter(f => f.endsWith('.json')))
  .map(f => (f.endsWith('.json') ? join(SCENARIOS, basename(f)) : join(SCENARIOS, `${f}.json`)));

let failed = 0;
for (const f of files) {
  try {
    const r = await runScenario(f, { model: values.model, turns: Number(values.turns) });
    if (!r.pass) failed++;
    console.log(`${r.pass ? '✅' : '❌'} ${r.scenario}: ${r.decision} score ${r.score} in ${r.turns} turns`);
    for (const i of r.issues) console.log(`     ${i.level}: ${i.rule} — ${i.message}`);
  } catch (err) {
    failed++;
    console.log(`❌ ${basename(f)}: ${err.message}`);
  }
}
console.log(`\n${files.length - failed}/${files.length} scenario(s) passed. Outputs in tools/eval/out/`);
process.exitCode = failed ? 1 : 0;
