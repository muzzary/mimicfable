"use strict";
/* Tests for bin/install.js. Run with: npm test (node --test).
 * Each test runs the real installer as a subprocess against a throwaway
 * sandbox via MIMICFABLE_HOME / MIMICFABLE_CWD, so nothing touches the
 * developer's actual config.
 */
const { test } = require("node:test");
const assert = require("node:assert");
const { execFileSync } = require("node:child_process");
const fs = require("fs");
const path = require("path");
const os = require("os");

const INSTALLER = path.join(__dirname, "..", "bin", "install.js");

function sandbox() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "mimicfable-test-"));
  const home = path.join(root, "home");
  const proj = path.join(root, "proj");
  fs.mkdirSync(home, { recursive: true });
  fs.mkdirSync(proj, { recursive: true });
  return { root, home, proj };
}

function run(sb, ...args) {
  return execFileSync(process.execPath, [INSTALLER, ...args], {
    encoding: "utf8",
    env: { ...process.env, MIMICFABLE_HOME: sb.home, MIMICFABLE_CWD: sb.proj },
  });
}

test("default install places agent and all four skills", (t) => {
  const sb = sandbox();
  t.after(() => fs.rmSync(sb.root, { recursive: true, force: true }));
  run(sb);
  assert.ok(fs.existsSync(path.join(sb.home, ".claude", "agents", "fable-engineer.md")));
  for (const skill of [
    "fable-problem-solving",
    "fable-code-craft",
    "fable-phase-planning",
    "fable-scope-control",
  ]) {
    assert.ok(
      fs.existsSync(path.join(sb.home, ".claude", "skills", skill, "SKILL.md")),
      `missing skill ${skill}`
    );
  }
});

test("rerun reports updated, not installed", (t) => {
  const sb = sandbox();
  t.after(() => fs.rmSync(sb.root, { recursive: true, force: true }));
  run(sb);
  const out = run(sb);
  assert.match(out, /updated/);
  assert.doesNotMatch(out, /installed {2}claude agent/);
});

test("gemini append preserves existing user content through install and uninstall", (t) => {
  const sb = sandbox();
  t.after(() => fs.rmSync(sb.root, { recursive: true, force: true }));
  const geminiFile = path.join(sb.home, ".gemini", "GEMINI.md");
  fs.mkdirSync(path.dirname(geminiFile), { recursive: true });
  fs.writeFileSync(geminiFile, "# My rules\nDo not delete me.\n");

  run(sb, "--gemini");
  const afterInstall = fs.readFileSync(geminiFile, "utf8");
  assert.match(afterInstall, /Do not delete me/);
  assert.match(afterInstall, /mimicfable:begin/);

  run(sb, "--uninstall");
  const afterUninstall = fs.readFileSync(geminiFile, "utf8");
  assert.match(afterUninstall, /Do not delete me/);
  assert.doesNotMatch(afterUninstall, /mimicfable:begin/);
});

test("cursor rule file gets frontmatter with alwaysApply", (t) => {
  const sb = sandbox();
  t.after(() => fs.rmSync(sb.root, { recursive: true, force: true }));
  run(sb, "--cursor");
  const mdc = fs.readFileSync(
    path.join(sb.proj, ".cursor", "rules", "mimicfable.mdc"),
    "utf8"
  );
  assert.ok(mdc.startsWith("---\n"), "frontmatter must be first");
  assert.match(mdc, /alwaysApply: true/);
  assert.match(mdc, /mimicfable:begin/);
});

test("uninstall removes everything including the cursor file", (t) => {
  const sb = sandbox();
  t.after(() => fs.rmSync(sb.root, { recursive: true, force: true }));
  run(sb, "--cursor", "--agents-md");
  run(sb); // claude files too
  run(sb, "--uninstall");
  assert.ok(!fs.existsSync(path.join(sb.home, ".claude", "agents", "fable-engineer.md")));
  assert.ok(!fs.existsSync(path.join(sb.proj, ".cursor", "rules", "mimicfable.mdc")));
  assert.ok(!fs.existsSync(path.join(sb.proj, "AGENTS.md")));
});

test("--skills does not install the agent, --agent does not install skills", (t) => {
  const sb = sandbox();
  t.after(() => fs.rmSync(sb.root, { recursive: true, force: true }));
  run(sb, "--skills");
  assert.ok(!fs.existsSync(path.join(sb.home, ".claude", "agents", "fable-engineer.md")));
  const sb2 = sandbox();
  t.after(() => fs.rmSync(sb2.root, { recursive: true, force: true }));
  run(sb2, "--agent");
  assert.ok(fs.existsSync(path.join(sb2.home, ".claude", "agents", "fable-engineer.md")));
  assert.ok(!fs.existsSync(path.join(sb2.home, ".claude", "skills", "fable-code-craft")));
});
