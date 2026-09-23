function unquote(v) {
  const s = v.trim();
  if ((s.startsWith("'") && s.endsWith("'")) || (s.startsWith('"') && s.endsWith('"'))) {
    const inner = s.slice(1, -1);
    return s.startsWith("'") ? inner.replace(/''/g, "'") : inner.replace(/\\"/g, '"');
  }
  return s;
}

// Top-level scalar keys of a YAML document (enough for frontmatter and workflow.yaml headers).
export function parseYamlScalars(text) {
  const out = {};
  for (const line of text.split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (m && m[2] !== '') out[m[1]] = unquote(m[2]);
  }
  return out;
}

export function parseFrontmatter(text) {
  const m = text.match(/^\uFEFF?---\r?\n([\s\S]*?)\r?\n---/);
  return m ? parseYamlScalars(m[1]) : {};
}

// Sets (or appends) top-level `key: "value"` lines in a YAML file, preserving everything else.
export function setYamlScalars(text, values) {
  let out = text.replace(/^\{\}\s*$/m, '');
  for (const [key, value] of Object.entries(values)) {
    const line = `${key}: ${JSON.stringify(value)}`;
    const re = new RegExp(`^${key}:.*$`, 'm');
    out = re.test(out) ? out.replace(re, line) : `${out.replace(/\s*$/, '')}\n${line}\n`;
  }
  return out;
}
