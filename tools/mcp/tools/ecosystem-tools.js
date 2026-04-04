import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';
import { readdirSync, statSync } from 'node:fs';

export function registerEcosystemTools(server, discovery, projectRoot) {
  const homedir = process.env.HOME || process.env.USERPROFILE;
  const claudeDir = join(homedir, '.claude');

  // Tool: List ecosystem catalog summary
  server.tool(
    'mdan_ecosystem_catalog',
    'Browse the full Claude Code ecosystem catalog — 1,053 skills, 418 agents, 340 commands, 67 hooks, 67 settings, 69 MCPs. Returns categorized summary.',
    {},
    async () => {
      const catalogPath = join(projectRoot, '_mdan', 'ecosystem', 'catalog', 'CATALOG.md');
      let catalog = 'Catalog not found. Run ecosystem module installation first.';
      if (existsSync(catalogPath)) {
        catalog = await readFile(catalogPath, 'utf-8');
        // Truncate if too long for MCP response
        if (catalog.length > 15000) {
          catalog = catalog.substring(0, 15000) + '\n\n... [truncated — read full catalog at ' + catalogPath + ']';
        }
      }
      return { content: [{ type: 'text', text: catalog }] };
    }
  );

  // Tool: Search ecosystem skills
  server.tool(
    'mdan_ecosystem_search-skills',
    'Search for skills by keyword in the ecosystem. Returns matching skill names.',
    {
      query: { type: 'string', description: 'Keyword to search for (e.g., "react", "security", "bioinformatics")' }
    },
    async ({ query }) => {
      const skillsDir = join(claudeDir, 'skills');
      if (!existsSync(skillsDir)) {
        return { content: [{ type: 'text', text: 'Skills directory not found at ' + skillsDir }] };
      }

      const q = query.toLowerCase();
      const matches = [];

      try {
        const dirs = readdirSync(skillsDir);
        for (const dir of dirs) {
          if (dir.toLowerCase().includes(q)) {
            matches.push(dir);
            continue;
          }
          // Check SKILL.md content for keyword match
          const skillFile = join(skillsDir, dir, 'SKILL.md');
          if (existsSync(skillFile)) {
            try {
              const content = await readFile(skillFile, 'utf-8');
              const first200 = content.substring(0, 200).toLowerCase();
              if (first200.includes(q)) {
                matches.push(dir);
              }
            } catch {}
          }
        }
      } catch {}

      return {
        content: [{
          type: 'text',
          text: matches.length > 0
            ? `Found ${matches.length} skills matching "${query}":\n\n${matches.map(m => `- ${m}`).join('\n')}\n\nTo use: Skill(skill: "${matches[0]}")`
            : `No skills found matching "${query}". Try a broader keyword or check ~/.claude/CATALOG.md`
        }]
      };
    }
  );

  // Tool: Search ecosystem agents
  server.tool(
    'mdan_ecosystem_search-agents',
    'Search for agent templates by keyword. Returns matching agent paths.',
    {
      query: { type: 'string', description: 'Keyword to search (e.g., "python", "devops", "security")' }
    },
    async ({ query }) => {
      const agentsDir = join(claudeDir, 'agents');
      if (!existsSync(agentsDir)) {
        return { content: [{ type: 'text', text: 'Agents directory not found at ' + agentsDir }] };
      }

      const q = query.toLowerCase();
      const matches = [];

      try {
        const categories = readdirSync(agentsDir);
        for (const cat of categories) {
          const catPath = join(agentsDir, cat);
          if (!statSync(catPath).isDirectory()) continue;
          const files = readdirSync(catPath);
          for (const file of files) {
            if (file.endsWith('.md') && (file.toLowerCase().includes(q) || cat.toLowerCase().includes(q))) {
              matches.push(`${cat}/${file.replace('.md', '')}`);
            }
          }
        }
      } catch {}

      return {
        content: [{
          type: 'text',
          text: matches.length > 0
            ? `Found ${matches.length} agents matching "${query}":\n\n${matches.map(m => `- ${m}`).join('\n')}\n\nTo use: Read ~/.claude/agents/${matches[0]}.md then spawn Agent with instructions.`
            : `No agents found matching "${query}".`
        }]
      };
    }
  );

  // Tool: Search ecosystem commands
  server.tool(
    'mdan_ecosystem_search-commands',
    'Search for command templates by keyword. Returns matching command paths.',
    {
      query: { type: 'string', description: 'Keyword to search (e.g., "deploy", "test", "git")' }
    },
    async ({ query }) => {
      const commandsDir = join(claudeDir, 'commands');
      if (!existsSync(commandsDir)) {
        return { content: [{ type: 'text', text: 'Commands directory not found at ' + commandsDir }] };
      }

      const q = query.toLowerCase();
      const matches = [];

      try {
        const categories = readdirSync(commandsDir);
        for (const cat of categories) {
          const catPath = join(commandsDir, cat);
          if (!statSync(catPath).isDirectory()) continue;
          const files = readdirSync(catPath);
          for (const file of files) {
            if (file.endsWith('.md') && (file.toLowerCase().includes(q) || cat.toLowerCase().includes(q))) {
              matches.push(`${cat}/${file.replace('.md', '')}`);
            }
          }
        }
      } catch {}

      return {
        content: [{
          type: 'text',
          text: matches.length > 0
            ? `Found ${matches.length} commands matching "${query}":\n\n${matches.map(m => `- ${m}`).join('\n')}`
            : `No commands found matching "${query}".`
        }]
      };
    }
  );

  // Tool: Read a skill's content
  server.tool(
    'mdan_ecosystem_read-skill',
    'Read the full content of a specific skill by name.',
    {
      name: { type: 'string', description: 'Skill name (e.g., "react-best-practices", "scanpy")' }
    },
    async ({ name }) => {
      const skillFile = join(claudeDir, 'skills', name, 'SKILL.md');
      if (!existsSync(skillFile)) {
        return { content: [{ type: 'text', text: `Skill "${name}" not found at ${skillFile}` }] };
      }
      const content = await readFile(skillFile, 'utf-8');
      return { content: [{ type: 'text', text: content }] };
    }
  );

  // Tool: Read an agent template
  server.tool(
    'mdan_ecosystem_read-agent',
    'Read the full content of an agent template by category/name.',
    {
      path: { type: 'string', description: 'Agent path as category/name (e.g., "security/penetration-tester")' }
    },
    async ({ path }) => {
      const agentFile = join(claudeDir, 'agents', path + '.md');
      if (!existsSync(agentFile)) {
        return { content: [{ type: 'text', text: `Agent "${path}" not found at ${agentFile}` }] };
      }
      const content = await readFile(agentFile, 'utf-8');
      return { content: [{ type: 'text', text: content }] };
    }
  );

  // Tool: List ecosystem stats
  server.tool(
    'mdan_ecosystem_stats',
    'Show ecosystem component statistics and installation status.',
    {},
    async () => {
      const stats = {};
      const dirs = {
        skills: join(claudeDir, 'skills'),
        agents: join(claudeDir, 'agents'),
        commands: join(claudeDir, 'commands'),
        hooks: join(claudeDir, 'hooks', 'aitmpl'),
        settings: join(claudeDir, 'settings-templates'),
        mcps: join(claudeDir, 'mcp-templates')
      };

      for (const [name, dir] of Object.entries(dirs)) {
        if (existsSync(dir)) {
          try {
            const count = readdirSync(dir, { recursive: true })
              .filter(f => f.endsWith('.md') || f.endsWith('.json')).length;
            stats[name] = { installed: true, count };
          } catch {
            stats[name] = { installed: true, count: '?' };
          }
        } else {
          stats[name] = { installed: false, count: 0 };
        }
      }

      const text = `# Ecosystem Status\n\n` +
        Object.entries(stats).map(([name, s]) =>
          `- **${name}**: ${s.installed ? `✅ ${s.count} components` : '❌ Not installed'}`
        ).join('\n') +
        `\n\nSources:\n- khalilbenaz/claude-skills-collection\n- davila7/claude-code-templates (aitmpl.com)`;

      return { content: [{ type: 'text', text }] };
    }
  );
}
