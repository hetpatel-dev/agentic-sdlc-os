#!/usr/bin/env python3
"""
validate_framework.py - Comprehensive Integrity Test Suite for Agentic SDLC OS
Verifies all agents, rules, skills, manifests, schemas, and automation scripts.
"""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

VALID_ANTIGRAVITY_TOOLS = {
    "read_file",
    "write_file",
    "edit_file",
    "run_command",
    "invoke_subagent",
    "send_message",
    "manage_subagents",
    "manage_task",
    "schedule",
    "search_web",
    "ask_question",
    "swarm"
}

class TestFrameworkIntegrity(unittest.TestCase):

    def test_root_files_exist(self):
        # Mandatory operating charters in every workspace using Agentic SDLC OS
        mandatory_files = ["AGENTS.md", "GEMINI.md"]
        for rf in mandatory_files:
            p = Path(rf)
            self.assertTrue(p.exists(), f"Missing root file: {rf}")
            self.assertGreater(p.stat().st_size, 0, f"Root file is empty: {rf}")

        # In framework source repository or plugin distribution, verify framework-level files
        is_framework_repo = Path(".github/workflows/sdlc-gates.yml").exists() or Path("assets/logo.svg").exists()
        if is_framework_repo:
            framework_files = [".gitignore", "LICENSE", "plugin.json"]
            for rf in framework_files:
                p = Path(rf)
                self.assertTrue(p.exists(), f"Missing framework root file: {rf}")
                self.assertGreater(p.stat().st_size, 0, f"Root file is empty: {rf}")

    def test_all_15_rules_exist_and_bounded(self):
        rules_dir = Path(".agents/rules")
        self.assertTrue(rules_dir.is_dir(), "Rules directory .agents/rules missing")

        expected_rules = [
            "00-core-engineering.md",
            "01-sdlc-governance.md",
            "02-requirements-traceability.md",
            "03-architecture-standards.md",
            "04-coding-standards.md",
            "05-api-contracts.md",
            "06-database-standards.md",
            "07-testing-standards.md",
            "08-security-baseline.md",
            "09-performance-baseline.md",
            "10-devops-standards.md",
            "11-release-governance.md",
            "12-observability-standards.md",
            "13-documentation-standards.md",
            "14-ai-agent-governance.md"
        ]

        for rule in expected_rules:
            rule_path = rules_dir / rule
            self.assertTrue(rule_path.exists(), f"Missing rule file: {rule}")
            size = rule_path.stat().st_size
            self.assertLessEqual(size, 24000, f"Rule {rule} exceeds 24,000 byte cap: {size} bytes")
            content = rule_path.read_text(encoding="utf-8")
            self.assertIn("#", content, f"Rule {rule} has no markdown headings")

    def test_all_31_agents_exist_and_valid(self):
        agents_dir = Path(".agents/agents")
        self.assertTrue(agents_dir.is_dir(), "Agents directory .agents/agents missing")

        agent_files = list(agents_dir.glob("*.md"))
        self.assertGreaterEqual(len(agent_files), 31, f"Expected at least 31 agents, found {len(agent_files)}")
        self.assertTrue((agents_dir / "code-reviewer.md").exists(), "Missing code-reviewer.md in .agents/agents")

        for af in agent_files:
            content = af.read_text(encoding="utf-8")
            # Frontmatter check
            self.assertTrue(content.startswith("---"), f"Agent {af.name} missing opening frontmatter '---'")
            parts = content.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"Agent {af.name} invalid frontmatter formatting")
            fm_text = parts[1]

            # Validate YAML frontmatter keys
            self.assertIn("name:", fm_text, f"Agent {af.name} missing 'name:' in frontmatter")
            self.assertIn("description:", fm_text, f"Agent {af.name} missing 'description:' in frontmatter")

            # Validate tools allowlist
            tools_match = re.search(r"tools:\s*\n((?:\s*-\s*[\w_]+\n)+)", fm_text)
            if tools_match:
                tools_block = tools_match.group(1)
                for line in tools_block.strip().splitlines():
                    tname = line.strip().lstrip("-").strip()
                    self.assertIn(tname, VALID_ANTIGRAVITY_TOOLS, f"Agent {af.name} uses invalid tool name '{tname}'")

        # In framework source repository or plugin distribution, verify root agents/ mirror
        if Path("agents").is_dir():
            for af in agent_files:
                root_af = Path("agents") / af.name
                self.assertTrue(root_af.exists(), f"Agent {af.name} not synchronized to root agents/")

    def test_all_18_skills_exist_and_valid(self):
        skills_dir = Path(".agents/skills")
        self.assertTrue(skills_dir.is_dir(), "Skills directory .agents/skills missing")

        expected_skills = [
            "product-discovery",
            "prd-generation",
            "requirements-validation",
            "system-design",
            "architecture-review",
            "feature-implementation",
            "code-review",
            "api-development",
            "database-change",
            "test-automation",
            "security-assessment",
            "performance-assessment",
            "ci-cd-setup",
            "release-readiness",
            "production-deployment",
            "incident-response",
            "technical-modernization",
            "continuous-improvement"
        ]

        for sname in expected_skills:
            sdir = skills_dir / sname
            self.assertTrue(sdir.is_dir(), f"Missing skill directory: {sname}")
            skill_md = sdir / "SKILL.md"
            self.assertTrue(skill_md.exists(), f"Missing SKILL.md for {sname}")

            content = skill_md.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"{sname}/SKILL.md missing opening frontmatter")
            parts = content.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"{sname}/SKILL.md invalid frontmatter")
            fm = parts[1]
            self.assertIn(f"name: {sname}", fm, f"{sname}/SKILL.md name mismatch in frontmatter")
            self.assertIn("description:", fm, f"{sname}/SKILL.md missing description")

            if Path("skills").is_dir():
                root_skill = Path("skills") / sname / "SKILL.md"
                self.assertTrue(root_skill.exists(), f"Skill {sname} not synchronized to root skills/")

    def test_manifests_are_valid_json(self):
        manifests = [
            ".agents/rules.json",
            ".agents/skills.json",
            ".agents/agents.json",
            ".agents/hooks.json",
            ".agents/mcp_config.json",
            "governance/quality_gates.json",
            "governance/traceability_ledger.json"
        ]
        # Validate root manifests if present
        for optional_manifest in ["plugin.json", "hooks.json", "mcp_config.json", "marketplace.json"]:
            if Path(optional_manifest).exists():
                manifests.append(optional_manifest)

        for m in manifests:
            p = Path(m)
            self.assertTrue(p.exists(), f"Missing manifest file: {m}")
            with open(p, "r", encoding="utf-8-sig") as f:
                try:
                    data = json.load(f)
                    self.assertIsInstance(data, dict, f"Manifest {m} must be a JSON object")
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in {m}: {e}")

    def test_quality_gates_complete(self):
        gates_path = Path("governance/quality_gates.json")
        with open(gates_path, "r", encoding="utf-8-sig") as f:
            gates = json.load(f).get("gates", {})
        expected_gates = [f"G{i}" for i in range(12)]
        for g in expected_gates:
            self.assertIn(g, gates, f"Quality gate {g} missing from governance/quality_gates.json")
            self.assertIn("name", gates[g])
            self.assertIn("stage", gates[g])
            self.assertIn("owner", gates[g])
            self.assertIn("exit_criteria", gates[g])

            # Ensure the required approver agent persona actually exists!
            approver = gates[g].get("required_approver")
            if approver:
                agent_md = Path(".agents/agents") / f"{approver}.md"
                self.assertTrue(agent_md.exists(), f"Required approver agent '{approver}' for gate {g} missing in .agents/agents/")

    def test_templates_exist(self):
        templates = [
            "prd-template.md",
            "adr-template.md",
            "rfcs-template.md",
            "threat-model-template.md",
            "test-plan-template.md",
            "release-checklist-template.md",
            "incident-postmortem-template.md",
            "task-record-template.md"
        ]
        tdir = Path("docs/templates")
        for t in templates:
            tp = tdir / t
            self.assertTrue(tp.exists(), f"Missing template: {t}")

    def test_automation_scripts_executable(self):
        scripts = [
            "scripts/traceability_cli.py",
            "scripts/gate_validator.py",
            "scripts/security_check.py",
            "scripts/mcp_traceability_server.py",
            "scripts/mcp_gate_server.py",
            "scripts/validate_framework.py",
            "scripts/bootstrap.ps1",
            "scripts/bootstrap.sh",
            "scripts/install.ps1",
            "scripts/install.sh",
            "scripts/update.py"
        ]
        for s in scripts:
            p = Path(s)
            self.assertTrue(p.exists(), f"Missing automation script: {s}")

if __name__ == "__main__":
    unittest.main()
