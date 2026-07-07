#!/usr/bin/env node
/* mimicfable installer
 *
 * Claude Code (default): copies the fable-engineer agent into ~/.claude/agents/
 * and the four fable skills into ~/.claude/skills/<name>/SKILL.md.
 *
 * Other coding agents: injects the portable instructions (PORTABLE.md) into the
 * file each tool reads, inside <!-- mimicfable --> marker comments so existing
 * content is never touched and reruns update in place.
 *
 * Usage:
 *   npx github:muzzary/mimicfable                Claude Code agent + skills
 *   npx github:muzzary/mimicfable --agent        Claude agent only
 *   npx github:muzzary/mimicfable --skills       Claude skills only
 *   npx github:muzzary/mimicfable --codex        ~/.codex/AGENTS.md (global)
 *   npx github:muzzary/mimicfable --copilot      .github/copilot-instructions.md (this project)
 *   npx github:muzzary/mimicfable --cursor       .cursor/rules/mimicfable.mdc (this project)
 *   npx github:muzzary/mimicfable --gemini       ~/.gemini/GEMINI.md (global)
 *   npx github:muzzary/mimicfable --agents-md    AGENTS.md (this project, universal standard)
 *   npx github:muzzary/mimicfable --uninstall    remove everything it installed
 */
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

const repoRoot = path.join(__dirname, "..");
// MIMICFABLE_HOME / MIMICFABLE_CWD exist so the installer can be tested in a sandbox.
const home = process.env.MIMICFABLE_HOME || os.homedir();
const cwd = process.env.MIMICFABLE_CWD || process.cwd();

const agentsDir = path.join(home, ".claude", "agents");
const skillsDir = path.join(home, ".claude", "skills");

const AGENT_FILE = "fable-engineer.md";
const SKILLS = [
  "fable-problem-solving",
  "fable-code-craft",
  "fable-phase-planning",
  "fable-scope-control",
];

const BEGIN = "<!-- mimicfable:begin (managed block, do not edit; rerun installer to update) -->";
const END = "<!-- mimicfable:end -->";

// Where each non-Claude tool reads instructions from.
const TARGETS = {
  codex: { file: () => path.join(home, ".codex", "AGENTS.md"), scope: "global" },
  copilot: {
    file: () => path.join(cwd, ".github", "copilot-instructions.md"),
    scope: "project",
  },
  cursor: {
    file: () => path.join(cwd, ".cursor", "rules", "mimicfable.mdc"),
    scope: "project",
  },
  gemini: { file: () => path.join(home, ".gemini", "GEMINI.md"), scope: "global" },
  "agents-md": { file: () => path.join(cwd, "AGENTS.md"), scope: "project" },
};

const args = process.argv.slice(2);
const has = (flag) => args.includes(flag);

if (has("--help") || has("-h")) {
  console.log(
    "mimicfable - install fable-style engineering instructions for coding agents\n\n" +
      "  (no flags)    Claude Code: agent + all four skills\n" +
      "  --agent       Claude Code: agent only\n" +
      "  --skills      Claude Code: skills only\n" +
      "  --codex       OpenAI Codex CLI (global ~/.codex/AGENTS.md)\n" +
      "  --copilot     GitHub Copilot (this project's .github/copilot-instructions.md)\n" +
      "  --cursor      Cursor (this project's .cursor/rules/mimicfable.mdc)\n" +
      "  --gemini      Gemini CLI (global ~/.gemini/GEMINI.md)\n" +
      "  --agents-md   plain AGENTS.md in this project (universal standard)\n" +
      "  --uninstall   remove everything mimicfable installed\n"
  );
  process.exit(0);
}

function portableBlock() {
  const body = fs.readFileSync(path.join(repoRoot, "PORTABLE.md"), "utf8").trim();
  return `${BEGIN}\n${body}\n${END}`;
}

// Insert or replace the marker block; never touch anything outside it.
function upsert(file) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const block = portableBlock();
  if (!fs.existsSync(file)) {
    fs.writeFileSync(file, block + "\n");
    return "installed";
  }
  const current = fs.readFileSync(file, "utf8");
  const begin = current.indexOf(BEGIN);
  const end = current.indexOf(END);
  if (begin !== -1 && end !== -1 && end > begin) {
    const updated =
      current.slice(0, begin) + block + current.slice(end + END.length);
    fs.writeFileSync(file, updated);
    return "updated";
  }
  fs.writeFileSync(file, current.trimEnd() + "\n\n" + block + "\n");
  return "appended to";
}

function removeBlock(file) {
  if (!fs.existsSync(file)) return false;
  const current = fs.readFileSync(file, "utf8");
  const begin = current.indexOf(BEGIN);
  const end = current.indexOf(END);
  if (begin === -1 || end === -1 || end <= begin) return false;
  const remainder = (
    current.slice(0, begin) + current.slice(end + END.length)
  ).trim();
  if (remainder === "") {
    fs.unlinkSync(file);
  } else {
    fs.writeFileSync(file, remainder + "\n");
  }
  return true;
}

function installClaudeAgent() {
  const dest = path.join(agentsDir, AGENT_FILE);
  fs.mkdirSync(agentsDir, { recursive: true });
  const existed = fs.existsSync(dest);
  fs.copyFileSync(path.join(repoRoot, AGENT_FILE), dest);
  console.log(`${existed ? "updated " : "installed"}  claude agent   ${dest}`);
}

function installClaudeSkill(name) {
  const src = path.join(repoRoot, "skills", `${name}.md`);
  if (!fs.existsSync(src)) {
    console.error(`missing in package: skills/${name}.md - skipped`);
    process.exitCode = 1;
    return;
  }
  const destDir = path.join(skillsDir, name);
  const dest = path.join(destDir, "SKILL.md");
  fs.mkdirSync(destDir, { recursive: true });
  const existed = fs.existsSync(dest);
  fs.copyFileSync(src, dest);
  console.log(`${existed ? "updated " : "installed"}  claude skill   ${dest}`);
}

function uninstall() {
  const agentDest = path.join(agentsDir, AGENT_FILE);
  if (fs.existsSync(agentDest)) {
    fs.unlinkSync(agentDest);
    console.log(`removed  claude agent   ${agentDest}`);
  }
  for (const name of SKILLS) {
    const destDir = path.join(skillsDir, name);
    if (fs.existsSync(path.join(destDir, "SKILL.md"))) {
      fs.rmSync(destDir, { recursive: true });
      console.log(`removed  claude skill   ${destDir}`);
    }
  }
  for (const [name, target] of Object.entries(TARGETS)) {
    if (removeBlock(target.file())) {
      console.log(`removed  ${name} block   ${target.file()}`);
    }
  }
  console.log("uninstall complete.");
}

try {
  if (has("--uninstall")) {
    uninstall();
    process.exit(process.exitCode || 0);
  }

  const otherTools = Object.keys(TARGETS).filter((t) => has(`--${t}`));
  const claudeOnlyFlags = has("--agent") || has("--skills");
  const wantClaude = otherTools.length === 0 || claudeOnlyFlags;

  if (wantClaude) {
    const wantAgent = has("--agent") || !has("--skills");
    const wantSkills = has("--skills") || !has("--agent");
    if (wantAgent) installClaudeAgent();
    if (wantSkills) SKILLS.forEach(installClaudeSkill);
  }

  for (const tool of otherTools) {
    const target = TARGETS[tool];
    const verb = upsert(target.file());
    console.log(`${verb}  ${tool} (${target.scope})   ${target.file()}`);
  }

  console.log(
    "\ndone." +
      (wantClaude
        ? " restart your Claude Code session so the agent/skills register." +
          "\nuse the agent by asking Claude to delegate to fable-engineer, or invoke" +
          "\nskills with /fable-problem-solving, /fable-code-craft," +
          "\n/fable-phase-planning, /fable-scope-control."
        : "") +
      (otherTools.length
        ? "\nother tools pick up their instructions file automatically on next run." +
          "\nproject-scope targets were written relative to the current directory."
        : "\ntip: --codex, --copilot, --cursor, --gemini, --agents-md install for other tools.")
  );
} catch (err) {
  console.error(`install failed: ${err.message}`);
  process.exit(1);
}
