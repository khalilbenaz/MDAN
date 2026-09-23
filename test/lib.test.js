import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseCsv, toCsv } from '../tools/lib/csv.js';
import { safeJoin, assertId } from '../tools/lib/paths.js';
import { parseFrontmatter, setYamlScalars, parseYamlScalars } from '../tools/lib/frontmatter.js';

test('csv round-trips commas, quotes, newlines and CRLF', () => {
  const rows = [{ a: 'x,y', b: 'say "hi"' }, { a: 'multi\nline', b: '' }];
  assert.deepEqual(parseCsv(toCsv(['a', 'b'], rows)), rows);
  assert.deepEqual(parseCsv('a,b\r\n1,2\r\n'), [{ a: '1', b: '2' }]);
});

test('safeJoin refuses traversal and absolute paths', () => {
  assert.throws(() => safeJoin('/base', '../etc/passwd'), /escapes/);
  assert.throws(() => safeJoin('/base', 'a/../../b'), /escapes/);
  assert.ok(safeJoin('/base', 'a/b.md').endsWith('b.md'));
});

test('assertId accepts DR-001 and rejects traversal', () => {
  assert.equal(assertId('DR-001'), 'DR-001');
  for (const bad of ['../x', 'a/b', '', '.hidden', 'a..b']) assert.throws(() => assertId(bad));
});

test('frontmatter and yaml scalars', () => {
  assert.deepEqual(parseFrontmatter("---\nname: 'it''s'\ndescription: \"a b\"\n---\nbody"), { name: "it's", description: 'a b' });
  const y = setYamlScalars('# c\n{}\n', { user_name: 'Khalil', communication_language: 'english' });
  assert.deepEqual(parseYamlScalars(y), { user_name: 'Khalil', communication_language: 'english' });
  assert.match(setYamlScalars('user_name: "a"\nx: 1\n', { user_name: 'b' }), /^user_name: "b"\nx: 1/);
});
