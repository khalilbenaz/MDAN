import { ContextGraph } from '../../cli/lib/context-graph.js';
import { join } from 'node:path';

export function registerGraphTools(server, projectRoot) {
  const graphPath = join(projectRoot, '_mdan/state/context-graph.json');

  server.tool(
    'mdan_graph_add-node',
    'Add an artifact node to the MDAN context graph',
    {
      id: { type: 'string', description: 'Unique node ID (e.g., prd-001)' },
      type: { type: 'string', description: 'Node type: artifact, decision, or debate' },
      path: { type: 'string', description: 'Path to the artifact file' },
      workflow: { type: 'string', description: 'Workflow that created this artifact' },
      agent: { type: 'string', description: 'Agent that created this artifact' },
    },
    async ({ id, type, path, workflow, agent }) => {
      const graph = ContextGraph.load(graphPath);
      graph.addNode({ id, type: type || 'artifact', path, created_by: { workflow, agent } });
      graph.save(graphPath);
      return { content: [{ type: 'text', text: `Node '${id}' added to context graph.` }] };
    }
  );

  server.tool(
    'mdan_graph_add-edge',
    'Add a relationship edge between two nodes in the context graph',
    {
      source: { type: 'string', description: 'Source node ID' },
      target: { type: 'string', description: 'Target node ID' },
      relation: { type: 'string', description: 'Relation type: input_to, derived_from, impacts, references' },
    },
    async ({ source, target, relation }) => {
      const graph = ContextGraph.load(graphPath);
      graph.addEdge({ source, target, relation });
      graph.save(graphPath);
      return { content: [{ type: 'text', text: `Edge ${source} --${relation}--> ${target} added.` }] };
    }
  );

  server.tool(
    'mdan_graph_impact',
    'Analyze downstream impact of an artifact in the context graph',
    {
      nodeId: { type: 'string', description: 'Node ID to analyze impact for' },
    },
    async ({ nodeId }) => {
      const graph = ContextGraph.load(graphPath);
      const downstream = graph.getDownstream(nodeId);
      return {
        content: [{
          type: 'text',
          text: `# Impact Analysis: ${nodeId}\n\n` +
            `**Downstream artifacts (${downstream.length}):**\n` +
            downstream.map(n => `- ${n.id} (${n.type}) → ${n.path || 'N/A'}`).join('\n') +
            (downstream.length === 0 ? '(no downstream dependencies)' : ''),
        }],
      };
    }
  );

  server.tool(
    'mdan_graph_visualize',
    'Generate a Mermaid diagram of the context graph',
    {},
    async () => {
      const graph = ContextGraph.load(graphPath);
      return { content: [{ type: 'text', text: graph.toMermaid() }] };
    }
  );
}
