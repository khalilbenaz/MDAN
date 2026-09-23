// Project state (_mdan/state/MDAN-STATE.json): current workflow + step, completed workflows,
// artifacts, decisions. Every write goes through a cross-process lock and an atomic rename.
import { readFileSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';
import { writeFileAtomic, withLock } from './fs-atomic.js';

export const statePathFor = projectRoot => join(projectRoot, '_mdan/state/MDAN-STATE.json');

// Recommended order of the method; used to suggest the next workflow.
export const PHASES = [
  { phase: '1-discover', workflows: ['create-product-brief', 'market-research', 'domain-research', 'technical-research'], required: ['create-product-brief'] },
  { phase: '2-plan', workflows: ['create-prd', 'create-ux-design'], required: ['create-prd'] },
  { phase: '3-architect', workflows: ['create-architecture', 'create-epics-and-stories'], required: ['create-architecture', 'create-epics-and-stories'] },
  { phase: '4-build', workflows: ['sprint-planning', 'dev-story', 'code-review'], required: ['sprint-planning'] },
  { phase: '5-ship', workflows: ['document-project'], required: [] },
];

function empty(projectRoot) {
  const now = new Date().toISOString();
  return {
    version: '4.1.0',
    project: { name: basename(projectRoot), created_at: now, last_updated: now },
    context_graph_path: '_mdan/state/context-graph.json',
    workflows_completed: [],
    current_workflow: null,
    artifacts: [],
    sessions: [],
    agent_sidecars: {},
    decisions: [],
    context_summary: '',
  };
}

export function loadState(projectRoot) {
  const file = statePathFor(projectRoot);
  if (!existsSync(file)) return empty(projectRoot);
  try {
    return { ...empty(projectRoot), ...JSON.parse(readFileSync(file, 'utf-8')) };
  } catch (err) {
    throw new Error(`Corrupted state ${file}: ${err.message}`);
  }
}

export function updateState(projectRoot, fn) {
  const file = statePathFor(projectRoot);
  return withLock(file, () => {
    const state = loadState(projectRoot);
    const result = fn(state);
    state.project.last_updated = new Date().toISOString();
    writeFileAtomic(file, JSON.stringify(state, null, 2) + '\n');
    return result ?? state;
  });
}

export function startWorkflow(state, workflow, { step = null, stepFile = null } = {}) {
  const now = new Date().toISOString();
  const resuming = state.current_workflow?.name === workflow;
  state.current_workflow = {
    name: workflow,
    step: step ?? (resuming ? state.current_workflow.step : null),
    step_file: stepFile ?? (resuming ? state.current_workflow.step_file : null),
    started_at: resuming ? state.current_workflow.started_at : now,
    updated_at: now,
  };
  state.sessions.push({ at: now, event: resuming ? 'resume' : 'start', workflow });
  state.sessions = state.sessions.slice(-200);
  return state.current_workflow;
}

export function setStep(state, workflow, step, stepFile = null) {
  if (state.current_workflow?.name !== workflow) startWorkflow(state, workflow);
  Object.assign(state.current_workflow, { step, step_file: stepFile, updated_at: new Date().toISOString() });
  return state.current_workflow;
}

export function completeWorkflow(state, workflow, { artifacts = [], summary = '' } = {}) {
  const now = new Date().toISOString();
  state.workflows_completed = state.workflows_completed.filter(w => w.name !== workflow);
  state.workflows_completed.push({ name: workflow, completed_at: now, artifacts });
  for (const a of artifacts) {
    state.artifacts = state.artifacts.filter(x => x.path !== a.path);
    state.artifacts.push({ ...a, workflow, created_at: now });
  }
  if (summary) state.context_summary = summary;
  if (state.current_workflow?.name === workflow) state.current_workflow = null;
  state.sessions.push({ at: now, event: 'complete', workflow });
  state.sessions = state.sessions.slice(-200);
}

export function recordDecision(state, { id, topic, decision }) {
  state.decisions = state.decisions.filter(d => d.id !== id);
  state.decisions.push({ id, topic, decision, at: new Date().toISOString() });
}

// First required workflow not completed yet, in method order, limited to installed workflows.
export function nextStep(state, installed = null) {
  const done = new Set(state.workflows_completed.map(w => w.name));
  if (state.current_workflow) {
    return { workflow: state.current_workflow.name, reason: 'resume', step: state.current_workflow.step };
  }
  for (const p of PHASES) {
    for (const wf of p.required) {
      if (installed && !installed.includes(wf)) continue;
      if (!done.has(wf)) return { workflow: wf, reason: 'next', phase: p.phase };
    }
  }
  return null;
}

export function summarize(state, installed = null) {
  const done = new Set(state.workflows_completed.map(w => w.name));
  return {
    project: state.project.name,
    current: state.current_workflow,
    phases: PHASES.map(p => ({
      phase: p.phase,
      workflows: p.workflows.filter(w => !installed || installed.includes(w)).map(w => ({ name: w, done: done.has(w) })),
    })),
    artifacts: state.artifacts,
    decisions: state.decisions,
    next: nextStep(state, installed),
  };
}
