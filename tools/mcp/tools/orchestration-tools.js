import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { existsSync } from 'node:fs';

export function registerOrchestrationTools(server, projectRoot) {
  server.tool(
    'mdan_orchestrate_party-mode',
    'Start a multi-agent party mode session. Modes: discussion, debate, consensus',
    {
      mode: { type: 'string', description: 'Orchestration mode: discussion, debate, or consensus' },
      topic: { type: 'string', description: 'Topic for the multi-agent session' },
      agents: { type: 'string', description: 'Comma-separated agent names to include (optional, defaults to all)' },
    },
    async ({ mode, topic, agents }) => {
      const partyPath = join(projectRoot, '_mdan/mdan/workflows/special/party-mode');
      const wizardContent = await readFile(join(partyPath, 'wizard.md'), 'utf-8');

      let modeStep = '';
      if (mode === 'debate') {
        const debatePath = join(partyPath, 'steps/step-02a-debate-mode.md');
        if (existsSync(debatePath)) {
          modeStep = await readFile(debatePath, 'utf-8');
        }
      } else if (mode === 'consensus') {
        const consensusPath = join(partyPath, 'steps/step-02b-consensus-mode.md');
        if (existsSync(consensusPath)) {
          modeStep = await readFile(consensusPath, 'utf-8');
        }
      }

      return {
        content: [{
          type: 'text',
          text: `# Multi-Agent Orchestration\n\n` +
            `**Mode:** ${mode || 'discussion'}\n` +
            `**Topic:** ${topic || '(ask the user)'}\n` +
            `**Agents:** ${agents || 'all installed'}\n\n` +
            `---\n\n${wizardContent}\n\n` +
            (modeStep ? `---\n\n## Mode-Specific Protocol:\n\n${modeStep}` : ''),
        }],
      };
    }
  );

  server.tool(
    'mdan_orchestrate_create-decision-record',
    'Create a decision record from a debate or consensus session',
    {
      id: { type: 'string', description: 'Decision record ID (e.g., DR-001)' },
      topic: { type: 'string', description: 'Decision topic' },
      mode: { type: 'string', description: 'Session mode: debate or consensus' },
      decision: { type: 'string', description: 'Final decision text' },
      rationale: { type: 'string', description: 'Rationale for the decision' },
      confidence: { type: 'number', description: 'Confidence score 0-1' },
      participants: { type: 'string', description: 'JSON string of participants object' },
      rounds: { type: 'string', description: 'JSON string of debate rounds array' },
      dissent: { type: 'string', description: 'Dissenting opinion if any' },
    },
    async ({ id, topic, mode, decision, rationale, confidence, participants, rounds, dissent }) => {
      const record = {
        id: id || `DR-${Date.now()}`,
        topic,
        mode: mode || 'debate',
        participants: participants ? JSON.parse(participants) : {},
        rounds: rounds ? JSON.parse(rounds) : [],
        decision,
        rationale,
        confidence: confidence || 0.5,
        dissent: dissent || null,
        date: new Date().toISOString(),
        registered_in_graph: false,
      };

      const outputDir = join(projectRoot, 'mdan_output/decisions');
      if (!existsSync(outputDir)) {
        await mkdir(outputDir, { recursive: true });
      }

      const outputPath = join(outputDir, `${record.id}.json`);
      await writeFile(outputPath, JSON.stringify(record, null, 2));

      return {
        content: [{
          type: 'text',
          text: `Decision record ${record.id} saved to ${outputPath}`,
        }],
      };
    }
  );
}
