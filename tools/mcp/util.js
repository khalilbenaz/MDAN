import { z } from 'zod';

export const text = (t, extra = {}) => ({ content: [{ type: 'text', text: t }], ...extra });

// Every tool handler goes through this: a thrown error becomes an MCP tool error, not a crash.
export function safe(fn) {
  return async (args, extra) => {
    try {
      return await fn(args ?? {}, extra);
    } catch (err) {
      return text(`Error: ${err.message}`, { isError: true });
    }
  };
}

// z.enum needs at least one value; fall back to a free string when nothing is installed.
export function nameSchema(names, description) {
  return (names.length ? z.enum(names) : z.string()).describe(description);
}
