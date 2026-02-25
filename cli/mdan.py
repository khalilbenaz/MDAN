#!/usr/bin/env python3
"""MDAN CLI - Multi-Agent Development Agentic Network"""

import os
import sys
import shutil
import json
from pathlib import Path

VERSION = "2.5.0"
MDAN_DIR = Path(__file__).parent.parent

# Colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
MAGENTA = "\033[0;35m"
BOLD = "\033[1m"
NC = "\033[0m"


def banner():
    print(f"{CYAN}")
    print("  ███╗   ███╗██████╗  █████╗ ███╗   ██╗")
    print("  ████╗ ████║██╔══██╗██╔══██╗████╗  ██║")
    print("  ██╔████╔██║██║  ██║███████║██╔██╗ ██║")
    print("  ██║╚██╔╝██║██║  ██║██╔══██║██║╚██╗██║")
    print("  ██║ ╚═╝ ██║██████╔╝██║  ██║██║ ╚████║")
    print("  ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝")
    print(f"{NC}")
    print(f"  {BOLD}Multi-Agent Development Agentic Network{NC} v{VERSION}\n")


def show_help():
    banner()
    print(f"{BOLD}USAGE{NC}")
    print("  mdan <command> [options]\n")
    print(f"{BOLD}COMMANDS{NC}")
    print("  init [name]              Create a new project")
    print("  attach [--rebuild]       Add MDAN to existing project")
    print("  status                   Show project status")
    print("  phase [1-5]              Show phase guide")
    print("  agent [name]             Show agent prompt")
    print("  oc                       Copy orchestrator prompt to clipboard")
    print("  skills                   List available skills")
    print("  version                  Show version\n")
    print(f"{BOLD}EXAMPLES{NC}")
    print("  mdan init my-app              # New project")
    print("  cd my-project && mdan attach  # Existing project")
    print("  mdan attach --rebuild         # Rebuild from scratch\n")
    print(f"{BOLD}AGENTS{NC}")
    print("  product, architect, ux, dev, test, security, devops, doc")


def cmd_init(name="my-project"):
    print(f"{CYAN}🚀 Creating: {BOLD}{name}{NC}")

    dirs = [
        f"{name}/mdan/agents",
        f"{name}/mdan/skills",
        f"{name}/mdan_output",
        f"{name}/.claude/skills",
        f"{name}/.github",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

    shutil.copy(f"{MDAN_DIR}/core/orchestrator.md", f"{name}/mdan/")
    shutil.copy(f"{MDAN_DIR}/core/universal-envelope.md", f"{name}/mdan/")

    for f in Path(f"{MDAN_DIR}/agents").glob("*.md"):
        shutil.copy(f, f"{name}/mdan/agents/")

    for f in Path(f"{MDAN_DIR}/templates").glob("*.md"):
        shutil.copy(f, f"{name}/mdan_output/")

    skills_dir = Path(f"{MDAN_DIR}/skills")
    if skills_dir.exists():
        for s in skills_dir.iterdir():
            if s.is_dir():
                shutil.copytree(s, f"{name}/mdan/skills/{s.name}", dirs_exist_ok=True)
                shutil.copytree(
                    s, f"{name}/.claude/skills/{s.name}", dirs_exist_ok=True
                )

    cursorrules = Path(f"{MDAN_DIR}/core/orchestrator.md").read_text()
    cursorrules += "\n\n## CURSOR INSTRUCTIONS\nAgent files in mdan/agents/\nSkills in mdan/skills/"
    Path(f"{name}/.cursorrules").write_text(cursorrules)
    shutil.copy(f"{name}/.cursorrules", f"{name}/.windsurfrules")
    shutil.copy(
        f"{MDAN_DIR}/core/orchestrator.md", f"{name}/.github/copilot-instructions.md"
    )
    Path(f"{name}/README.md").write_text(f"# {name}\n\n> Built with MDAN\n")

    print(f"{GREEN}✅ Created {name}/{NC}\n")
    print(f"  {BOLD}Next:{NC} cursor {name}")


def cmd_attach(rebuild=None):
    project = Path.cwd().name

    if rebuild == "--rebuild":
        print(f"{MAGENTA}🔄 REBUILD MODE: {BOLD}{project}{NC}")
    else:
        print(f"{CYAN}🔗 Attaching to: {BOLD}{project}{NC}")

    Path("mdan/agents").mkdir(parents=True, exist_ok=True)
    Path("mdan/skills").mkdir(parents=True, exist_ok=True)
    Path(".claude/skills").mkdir(parents=True, exist_ok=True)
    Path(".github").mkdir(parents=True, exist_ok=True)

    shutil.copy(f"{MDAN_DIR}/core/orchestrator.md", "mdan/")
    shutil.copy(f"{MDAN_DIR}/core/universal-envelope.md", "mdan/")

    for f in Path(f"{MDAN_DIR}/agents").glob("*.md"):
        shutil.copy(f, "mdan/agents/")

    skills_dir = Path(f"{MDAN_DIR}/skills")
    if skills_dir.exists():
        for s in skills_dir.iterdir():
            if s.is_dir():
                shutil.copytree(s, f"mdan/skills/{s.name}", dirs_exist_ok=True)
                shutil.copytree(s, f".claude/skills/{s.name}", dirs_exist_ok=True)

    cursorrules = Path(f"{MDAN_DIR}/core/orchestrator.md").read_text()
    if rebuild == "--rebuild":
        cursorrules += (
            "\n\n## REBUILD MODE\nAnalyze existing code then rewrite from scratch."
        )
    else:
        cursorrules += (
            "\n\n## EXISTING PROJECT\nAnalyze codebase before making changes."
        )
    Path(".cursorrules").write_text(cursorrules)
    shutil.copy(".cursorrules", ".windsurfrules")
    shutil.copy(f"{MDAN_DIR}/core/orchestrator.md", ".github/copilot-instructions.md")

    print(f"{GREEN}✅ MDAN ready!{NC}\n")
    print(f"  {BOLD}Next:{NC} Run {CYAN}mdan oc{NC} to copy prompt")
    if rebuild == "--rebuild":
        print(f"  Start: {CYAN}MDAN REBUILD: Analyze and rewrite this project{NC}")
    else:
        print(f"  Start: {CYAN}MDAN: Analyze this project{NC}")


def cmd_oc():
    import subprocess

    orch_file = Path("mdan/orchestrator.md")
    if not orch_file.exists():
        orch_file = Path(f"{MDAN_DIR}/core/orchestrator.md")

    if orch_file.exists():
        content = orch_file.read_text()
        try:
            if sys.platform == "darwin":
                subprocess.run(
                    "pbcopy", universal_newlines=True, input=content, check=True
                )
            elif sys.platform == "win32":
                subprocess.run(
                    "clip", universal_newlines=True, input=content, check=True
                )
            elif sys.platform == "linux":
                if shutil.which("xclip"):
                    subprocess.run(
                        ["xclip", "-selection", "clipboard"],
                        universal_newlines=True,
                        input=content,
                        check=True,
                    )
                elif shutil.which("wl-copy"):
                    subprocess.run(
                        ["wl-copy"], universal_newlines=True, input=content, check=True
                    )
                else:
                    raise Exception("No clipboard tool found")
            print(f"{GREEN}✅ Orchestrator prompt copied to clipboard!{NC}")
            print("   Paste it into Claude, ChatGPT, or your favorite LLM.")
        except Exception:
            print(content)
            print(
                f"\n{YELLOW}⚠️  Could not copy to clipboard automatically. Please copy the text above.{NC}"
            )
    else:
        print(f"{RED}Orchestrator file not found.{NC}")


def cmd_status():
    if Path("mdan/orchestrator.md").exists():
        print(f"{GREEN}✅ MDAN is active in this project{NC}")
        if Path("mdan/STATUS.md").exists():
            print(Path("mdan/STATUS.md").read_text())
    else:
        print(f"{YELLOW}No MDAN project here.{NC}")
        print("  Run: mdan init [name]  or  mdan attach")


def cmd_phase(num, action=None):
    import subprocess

    phases = {
        "1": ("01-discover.md", "DISCOVER"),
        "discover": ("01-discover.md", "DISCOVER"),
        "2": ("02-design.md", "DESIGN"),
        "design": ("02-design.md", "DESIGN"),
        "3": ("03-build.md", "BUILD"),
        "build": ("03-build.md", "BUILD"),
        "4": ("04-verify.md", "VERIFY"),
        "verify": ("04-verify.md", "VERIFY"),
        "5": ("05-ship.md", "SHIP"),
        "ship": ("05-ship.md", "SHIP"),
    }

    if num not in phases:
        print("Usage: mdan phase [1-5|name] [copy]")
        return

    file, name = phases[num]
    phase_file = Path(f"{MDAN_DIR}/phases/{file}")

    if phase_file.exists():
        content = phase_file.read_text()
        if action in ["copy", "-c"]:
            try:
                if sys.platform == "darwin":
                    subprocess.run(
                        "pbcopy", universal_newlines=True, input=content, check=True
                    )
                elif sys.platform == "win32":
                    subprocess.run(
                        "clip", universal_newlines=True, input=content, check=True
                    )
                elif sys.platform == "linux":
                    if shutil.which("xclip"):
                        subprocess.run(
                            ["xclip", "-selection", "clipboard"],
                            universal_newlines=True,
                            input=content,
                            check=True,
                        )
                    elif shutil.which("wl-copy"):
                        subprocess.run(
                            ["wl-copy"],
                            universal_newlines=True,
                            input=content,
                            check=True,
                        )
                    else:
                        raise Exception("No clipboard tool found")
                print(f"{GREEN}✅ Phase {name} prompt copied to clipboard!{NC}")
                print("   Paste it into your LLM to start the phase.")
            except Exception:
                print(content)
                print(
                    f"\n{YELLOW}⚠️  Could not copy automatically. Please copy the text above.{NC}"
                )
        else:
            print(f"{CYAN}{BOLD}Phase {name}{NC}")
            print(content)
            print(
                f"\n{YELLOW}Tip: Run '{CYAN}mdan phase {num} copy{YELLOW}' to copy this content to clipboard.{NC}"
            )
    else:
        print(f"Phase file not found: {file}")


def cmd_agent(name):
    file = Path(f"{MDAN_DIR}/agents/{name}.md")
    if file.exists():
        print(file.read_text())
    else:
        print("Agents: product, architect, ux, dev, test, security, devops, doc")


def cmd_skills():
    print(f"{CYAN}Skills:{NC}")
    skills_dir = Path(f"{MDAN_DIR}/skills")
    if skills_dir.exists():
        for s in skills_dir.iterdir():
            print(f"  {s.name}")
    else:
        print("  No skills installed")


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "help"

    if cmd in ["help", "--help", "-h", None]:
        show_help()
    elif cmd == "init":
        cmd_init(args[1] if len(args) > 1 else "my-project")
    elif cmd == "attach":
        cmd_attach(args[1] if len(args) > 1 else None)
    elif cmd == "oc":
        cmd_oc()
    elif cmd == "status":
        cmd_status()
    elif cmd == "phase":
        cmd_phase(
            args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None
        )
    elif cmd == "agent":
        cmd_agent(args[1] if len(args) > 1 else None)
    elif cmd == "skills":
        cmd_skills()
    elif cmd in ["version", "-v"]:
        print(f"MDAN v{VERSION}")
    else:
        print(f"Unknown: {cmd}. Run: mdan help")


if __name__ == "__main__":
    main()
