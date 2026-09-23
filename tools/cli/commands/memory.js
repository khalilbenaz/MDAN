import { recall, forget, listSidecars } from '../../lib/memory.js';
import { projectRootFromEnv } from '../../lib/paths.js';

export const help = `Usage: mdan memory                     List agents with memories
       mdan memory <agent> [query]       Show an agent's memories
       mdan memory <agent> --forget <id> Delete a memory`;

export default async function memory(args) {
  if (args.includes('--help') || args.includes('-h')) return console.log(help);
  const root = projectRootFromEnv();
  const [agent, ...rest] = args;

  if (!agent) {
    const agents = listSidecars(root);
    return console.log(agents.length ? agents.join('\n') : 'No agent memory yet.');
  }
  const forgetIdx = rest.indexOf('--forget');
  if (forgetIdx !== -1) {
    forget(root, agent, rest[forgetIdx + 1]);
    return console.log(`Deleted memory ${rest[forgetIdx + 1]}.`);
  }
  const { sidecar, memories } = recall(root, agent, { query: rest.join(' '), limit: 50 });
  console.log(`🧠 ${agent} — ${sidecar.sessions_participated} session(s), ${sidecar.memories.length} memories\n`);
  for (const m of memories) console.log(`  [${m.id}] ${m.type.padEnd(11)} ${m.confidence.toFixed(2)}  ${m.content}`);
}
