// Scale-adaptive routing: decides how much ceremony a change needs, using the context graph's real
// blast radius (downstream artifacts) instead of text heuristics alone.
import { ContextGraph, graphPathFor } from '../cli/lib/context-graph.js';
import { detectScale } from './quality.js';

const RISK_TERMS = [
  [/\b(migration|schema|database|base de donn[ée]es|sql)\b/i, 'data/schema change'],
  [/\b(auth|authentification|login|permission|rbac|oauth|jwt|password|mot de passe)\b/i, 'security-sensitive'],
  [/\b(payment|paiement|wallet|ledger|transaction|virement|transfer|solde|balance)\b/i, 'money movement'],
  [/\b(breaking|public api|contrat|contract|versioning|backward)\b/i, 'contract change'],
  [/\b(architecture|refactor(ing)?|r[ée]architect|microservice|monolith)\b/i, 'architectural'],
  [/\b(rgpd|gdpr|pci|kyc|aml|compliance|conformit[ée]|bam)\b/i, 'regulatory'],
];

export const ROUTES = {
  oneshot: { workflow: 'quick-dev', label: 'Direct implementation (quick-dev), self-check + adversarial review' },
  spec: { workflow: 'quick-spec', label: 'Tech spec first (quick-spec), then quick-dev' },
  full: { workflow: 'correct-course', fallback: 'create-prd', label: 'Full planning: update PRD/architecture/epics (correct-course, or create-prd for a new product)' },
};

/**
 * @param {object} input
 * @param {string} input.description  What the change is about.
 * @param {string[]} [input.files]    Files expected to change.
 * @param {string[]} [input.artifacts] Context graph node ids touched (e.g. prd, architecture).
 */
export function estimateScope(projectRoot, { description = '', files = [], artifacts = [] }) {
  const reasons = [];
  let points = 0;

  const risks = RISK_TERMS.filter(([re]) => re.test(description)).map(([, label]) => label);
  if (risks.length) { points += risks.length * 2; reasons.push(`risk: ${risks.join(', ')}`); }

  if (files.length > 10) { points += 4; reasons.push(`${files.length} files`); }
  else if (files.length > 2) { points += 2; reasons.push(`${files.length} files`); }
  else if (files.length) reasons.push(`${files.length} file(s)`);

  const graph = ContextGraph.load(graphPathFor(projectRoot));
  const unknown = artifacts.filter(id => !graph.getNode(id));
  const downstream = new Set(artifacts.filter(id => graph.getNode(id)).flatMap(id => graph.getDownstream(id).map(n => n.id)));
  if (downstream.size) {
    points += downstream.size > 3 ? 4 : 2;
    reasons.push(`impacts ${downstream.size} downstream artifact(s): ${[...downstream].slice(0, 6).join(', ')}`);
  }
  if (artifacts.some(id => /prd|archi/i.test(id))) { points += 3; reasons.push('touches PRD/architecture'); }

  const words = description.trim().split(/\s+/).filter(Boolean).length;
  if (words > 120) { points += 1; reasons.push('long description'); }

  const { scale } = detectScale(projectRoot);
  // Bigger organisations get more ceremony for the same change.
  const thresholds = { solo: [3, 8], team: [2, 6], enterprise: [1, 4] }[scale];
  const route = points <= thresholds[0] ? 'oneshot' : points <= thresholds[1] ? 'spec' : 'full';

  return {
    route,
    points,
    scale,
    ...ROUTES[route],
    reasons: reasons.length ? reasons : ['small, low-risk change'],
    downstream: [...downstream],
    unknownArtifacts: unknown,
  };
}
