#!/usr/bin/env node
/* mimicfable installer
 *
 * Copies the fable-engineer agent into ~/.claude/agents/ and the four fable
 * skills into ~/.claude/skills/<name>/SKILL.md, where Claude Code discovers
 * them. No dependencies, no network calls: everything ships inside this repo.
 *
 * Usage:
 *   npx github:muzzary/mimicfable            install agent + skills
 *   npx github:muzzary/mimicfable --skills   skills only
 *   npx github:muzzary/mimicfable --agent    agent only
 *   npx github:muzzary/mimicfable --uninstall remove everything it installed
 */
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

const repoRoot = path.join(__dirname, "..");
// MIMICFABLE_HOME exists so the installer can be tested against a sandbox dir.
const home = process.env.MIMICFABLE_HOME || os.homedir();
const agentsDir = path.join(home, ".claude", "agents");
const skillsDir = path.join(home, ".claude", "skills");

const AGENT_FILE = "fable-engineer.md";
const SKILLS = [
  "fable-problem-solving",
  "fable-code-craft",
  "fable-phase-planning",
  "fable-scope-control",
];

const args = process.argv.slice(2);
const has = (flag) => args.includes(flag);

if (has("--help") || has("-h")) {
  console.log(
    "mimicfable - install the fable-engineer agent and fable skills for Claude Code\n\n" +
      "  (no flags)    install agent + all four skills\n" +
      "  --agent       install only the agent\n" +
      "  --skills      install only the skills\n" +
      "  --uninstall   remove previously installed agent and skills\n"
  );
  process.exit(0);
}

const wantAgent = has("--agent") || !has("--skills");
const wantSkills = has("--skills") || !has("--agent");

function installAgent() {
  const src = path.join(repoRoot, AGENT_FILE);
  const dest = path.join(agentsDir, AGENT_FILE);
  fs.mkdirSync(agentsDir, { recursive: true });
  const existed = fs.existsSync(dest);
  fs.copyFileSync(src, dest);
  console.log(`${existed ? "updated " : "installed"}  agent  ${dest}`);
}

function installSkill(name) {
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
  console.log(`${existed ? "updated " : "installed"}  skill  ${dest}`);
}

function uninstall() {
  const agentDest = path.join(agentsDir, AGENT_FILE);
  if (fs.existsSync(agentDest)) {
    fs.unlinkSync(agentDest);
    console.log(`removed  agent  ${agentDest}`);
  }
  for (const name of SKILLS) {
    const destDir = path.join(skillsDir, name);
    if (fs.existsSync(path.join(destDir, "SKILL.md"))) {
      fs.rmSync(destDir, { recursive: true });
      console.log(`removed  skill  ${destDir}`);
    }
  }
  console.log("uninstall complete.");
}

try {
  if (has("--uninstall")) {
    uninstall();
  } else {
    if (wantAgent) installAgent();
    if (wantSkills) SKILLS.forEach(installSkill);
    console.log(
      "\ndone. restart your Claude Code session so the new agent/skills register.\n" +
        "use the agent by asking Claude to delegate to fable-engineer, or invoke\n" +
        "skills with /fable-problem-solving, /fable-code-craft, /fable-phase-planning,\n" +
        "/fable-scope-control."
    );
  }
} catch (err) {
  console.error(`install failed: ${err.message}`);
  process.exit(1);
}
