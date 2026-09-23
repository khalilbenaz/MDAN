import { parseArgs } from 'node:util';
import { resolve } from 'node:path';
import { writeBundles } from '../../lib/bundle.js';
import { readAgents } from '../../lib/sources.js';
import { PACKAGE_ROOT } from '../../lib/paths.js';
import { resolveRoots } from '../../mcp/server.js';

export const help = `Usage: mdan bundle [agent ...] [--all] [--out dist/bundles] [--lang "<language>"]

Builds web bundles (instructions + knowledge file) for ChatGPT custom GPTs, Gemini Gems or Claude Projects.
Without agents: mdan-master. --all: every installed agent.`;

export default async function bundle(argv) {
  const { values, positionals } = parseArgs({
    args: argv,
    allowPositionals: true,
    options: { all: { type: 'boolean' }, out: { type: 'string' }, lang: { type: 'string' }, help: { type: 'boolean', short: 'h' } },
  });
  if (values.help) return console.log(help);
  const { contentRoot } = await resolveRoots();
  const agents = values.all ? readAgents(contentRoot).map(a => a.name) : positionals.length ? positionals : ['mdan-master'];
  const out = resolve(values.out || 'dist/bundles');
  const results = writeBundles(contentRoot || PACKAGE_ROOT, agents, out, { language: values.lang });
  for (const r of results) console.log(`✔ ${r.agent}: ${r.files} files → ${r.agent}.instructions.md (${r.instructionsChars} chars) + ${r.agent}.knowledge.md (${Math.round(r.knowledgeChars / 1024)} KB)`);
  console.log(`\nBundles in ${out} — see README.md there for ChatGPT / Gemini / Claude setup.`);
}
