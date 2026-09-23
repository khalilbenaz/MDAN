import { findBrokenRefs } from '../../lib/refs.js';
import { projectRootFromEnv } from '../../lib/paths.js';

export default async function validate(args) {
  if (args.includes('--help') || args.includes('-h')) {
    return console.log('Usage: mdan validate\n\nChecks that every {project-root}/... and relative step reference in _mdan resolves to an existing file.');
  }
  const broken = findBrokenRefs(projectRootFromEnv(), ['_mdan']);
  for (const b of broken) console.log(`${b.file}: ${b.ref}`);
  console.log(broken.length ? `\n${broken.length} broken reference(s)` : 'All references resolve.');
  if (broken.length) process.exitCode = 1;
}
