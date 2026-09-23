// Web bundles: package an agent (persona + rules + every workflow its menu references, with steps
// and templates) for ChatGPT custom GPTs, Gemini Gems or Claude Projects, where there is no IDE.
//   <agent>.instructions.md — short system prompt (fits the ~8k char instruction limit)
//   <agent>.knowledge.md    — full knowledge file, one section per source file, titled by its path
import { readFileSync, existsSync, readdirSync, statSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname, relative, sep } from 'node:path';
import { readAgents } from './sources.js';
import { safeJoin } from './paths.js';

const INSTRUCTIONS_LIMIT = 8000;
const toPosix = p => p.split(sep).join('/');

function filesUnder(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const name of readdirSync(dir).sort()) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...filesUnder(full));
    else if (/\.(md|xml|ya?ml|csv|json)$/.test(name)) out.push(full);
  }
  return out;
}

// Workflow files referenced by an agent menu (exec="…" / workflow="…"), with their whole folder.
function referencedWorkflowFiles(contentRoot, agentText) {
  const refs = [...agentText.matchAll(/(?:exec|workflow)="\{project-root\}\/([^"]+)"/g)].map(m => m[1]);
  const files = new Set();
  for (const ref of refs) {
    const full = safeJoin(contentRoot, ref);
    if (!existsSync(full)) continue;
    const folder = dirname(full);
    // A wizard owns its folder (steps/, templates/, data/); the special folders hold shared protocols too.
    for (const f of filesUnder(folder)) files.add(f);
    if (ref.endsWith('.yaml')) files.add(safeJoin(contentRoot, '_mdan/core/tasks/workflow.xml'));
  }
  return [...files];
}

export function bundleAgent(contentRoot, agentName, { language = null } = {}) {
  const agent = readAgents(contentRoot).find(a => a.name === agentName);
  if (!agent) throw new Error(`Unknown agent '${agentName}'`);
  const agentPath = join(contentRoot, agent.path);
  const agentText = readFileSync(agentPath, 'utf-8');
  const rulesPath = join(contentRoot, '_mdan/core/rules.md');

  const sources = [rulesPath, agentPath, ...referencedWorkflowFiles(contentRoot, agentText)];
  const knowledge = [
    `# MDAN knowledge bundle — ${agent.icon} ${agent.displayName} (${agent.title})`,
    '',
    'Each section below is one MDAN source file, titled with its path. A reference like `{project-root}/<path>` in the text means "the section titled <path>".',
    ...sources.filter(existsSync).map(f => `\n---\n\n## FILE: ${toPosix(relative(contentRoot, f))}\n\n${readFileSync(f, 'utf-8').trim()}\n`),
  ].join('\n');

  const workflows = [...agentText.matchAll(/<item cmd="([^"]+)"[^>]*(?:exec|workflow)="\{project-root\}\/([^"]+)"[^>]*>([^<]*)<\/item>/g)]
    .map(m => `- ${m[3].trim()} → section \`${m[2]}\``);

  let instructions = [
    `You are ${agent.displayName}, ${agent.title} of the MDAN method. ${agent.icon}`,
    '',
    `Role: ${agent.role}`,
    `Identity: ${agent.identity}`,
    `Communication style: ${agent.communicationStyle}`,
    `Principles: ${agent.principles}`,
    '',
    language ? `Always answer in: ${language}.` : 'Follow the language and communication rules in the knowledge section `_mdan/core/rules.md`.',
    '',
    'Your full definition, menu and workflows are in the attached knowledge file (sections titled "FILE: <path>").',
    `At the start, greet the user as ${agent.displayName}, show your numbered menu (section \`${agent.path}\`) and wait.`,
    'When a menu item is chosen, open the referenced section and execute that workflow step by step: one step at a time, stop at every menu, never skip steps.',
    'There is no file system: produce every document inline in the chat (or in a canvas) and tell the user where to save it.',
    '',
    workflows.length ? `Workflows:\n${workflows.join('\n')}` : '',
  ].join('\n');
  if (instructions.length > INSTRUCTIONS_LIMIT) instructions = `${instructions.slice(0, INSTRUCTIONS_LIMIT - 20)}\n…(truncated)`;

  return { agent: agent.name, instructions, knowledge, files: sources.length };
}

export function writeBundles(contentRoot, agentNames, outDir, options = {}) {
  mkdirSync(outDir, { recursive: true });
  const results = agentNames.map(name => {
    const b = bundleAgent(contentRoot, name, options);
    writeFileSync(join(outDir, `${name}.instructions.md`), b.instructions + '\n');
    writeFileSync(join(outDir, `${name}.knowledge.md`), b.knowledge + '\n');
    return { agent: name, files: b.files, instructionsChars: b.instructions.length, knowledgeChars: b.knowledge.length };
  });
  writeFileSync(join(outDir, 'README.md'), [
    '# MDAN web bundles',
    '',
    'For each agent:',
    '- **ChatGPT (custom GPT)**: paste `<agent>.instructions.md` into *Instructions*, upload `<agent>.knowledge.md` as *Knowledge*.',
    '- **Gemini (Gem)**: paste the instructions, add the knowledge file.',
    '- **Claude (Project)**: put the instructions in *Project instructions*, add the knowledge file to the project.',
    '',
    'Planning (brief, PRD, UX, architecture, epics) works well on the web; come back to the IDE (`npx mdan-method install`) to implement.',
    '',
    ...results.map(r => `- ${r.agent}: ${r.files} source files, ${r.knowledgeChars} chars of knowledge`),
    '',
  ].join('\n'));
  return results;
}
