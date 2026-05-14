#!/usr/bin/env python3
"""
Claude Code Python Orchestrator
================================

Demonstrates how to run Claude Code agents from Python using `claude -p`.

Three patterns shown:
  1. Simple prompt  — ask a question, get a text answer
  2. Structured     — get validated JSON back via --json-schema
  3. Parallel       — run multiple agents concurrently

Usage:
  python3 scripts/orchestrator.py                    # run all demos
  python3 scripts/orchestrator.py --demo simple      # just the simple demo
  python3 scripts/orchestrator.py --demo structured   # just structured JSON
  python3 scripts/orchestrator.py --demo parallel     # just parallel agents

Requirements:
  - Claude Code CLI installed and authenticated (`claude --version`)
  - Run from the repo root so agents/skills are discoverable
"""

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


# ---------------------------------------------------------------------------
# Core helper: call `claude -p`
# ---------------------------------------------------------------------------

def claude(
    prompt: str,
    *,
    output_format: str = "text",
    json_schema: dict | None = None,
    max_turns: int = 10,
    max_budget_usd: float | None = None,
    bare: bool = False,
    cwd: str | None = None,
) -> str | dict:
    """
    Call Claude Code in print mode and return the result.

    Args:
        prompt:        The prompt to send.
        output_format: "text" or "json".
        json_schema:   If set, validates output against this JSON schema.
        max_turns:     Max agentic turns before stopping.
        max_budget_usd: Optional cost cap per invocation.
        bare:          Skip auto-discovery of settings/MCP (faster startup).
        cwd:           Working directory for the subprocess.

    Returns:
        str if output_format="text", dict if output_format="json".
    """
    cmd = ["claude", "-p", prompt, "--output-format", output_format]
    cmd += ["--max-turns", str(max_turns)]

    if json_schema:
        cmd += ["--json-schema", json.dumps(json_schema)]
    if max_budget_usd is not None:
        cmd += ["--max-budget-usd", str(max_budget_usd)]
    if bare:
        cmd.append("--bare")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or str(Path(__file__).resolve().parent.parent),
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p failed (exit {result.returncode}):\n{result.stderr}"
        )

    if output_format == "json":
        envelope = json.loads(result.stdout)
        # `claude -p --output-format json` wraps output in an envelope:
        #   {"type": "result", "result": "...", "structured_output": {...}, ...}
        # - With --json-schema: validated data is in "structured_output"
        # - Without: the text response is in "result"
        if json_schema:
            return envelope.get("structured_output", {})
        return envelope
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Demo 1: Simple prompt
# ---------------------------------------------------------------------------

def demo_simple():
    """Ask Claude a plain question — text in, text out."""
    print("=" * 60)
    print("DEMO 1: Simple Prompt")
    print("=" * 60)

    answer = claude(
        "What files are in the tutorial/ directory? List them briefly.",
        max_turns=3,
    )
    print(answer)
    print()


# ---------------------------------------------------------------------------
# Demo 2: Structured JSON with schema validation
# ---------------------------------------------------------------------------

WEATHER_SCHEMA = {
    "type": "object",
    "properties": {
        "city":          {"type": "string"},
        "temp_celsius":  {"type": "number"},
        "conditions":    {"type": "string"},
        "humidity_pct":  {"type": "number"},
        "source":        {"type": "string"},
    },
    "required": ["city", "temp_celsius", "conditions"],
}

def demo_structured():
    """Get validated JSON back — Claude's output must match the schema."""
    print("=" * 60)
    print("DEMO 2: Structured JSON Output")
    print("=" * 60)

    weather = claude(
        "Fetch the current weather for Dubai using the Open-Meteo API. "
        "Endpoint: https://api.open-meteo.com/v1/forecast"
        "?latitude=25.2048&longitude=55.2708"
        "&current=temperature_2m,relative_humidity_2m",
        output_format="json",
        json_schema=WEATHER_SCHEMA,
        max_turns=5,
    )

    print(f"  City:        {weather.get('city', 'N/A')}")
    print(f"  Temperature: {weather.get('temp_celsius', 'N/A')}°C")
    print(f"  Conditions:  {weather.get('conditions', 'N/A')}")
    print(f"  Humidity:    {weather.get('humidity_pct', 'N/A')}%")
    print(f"  Source:      {weather.get('source', 'N/A')}")
    print()


# ---------------------------------------------------------------------------
# Demo 3: Parallel agents
# ---------------------------------------------------------------------------

PARALLEL_TASKS = [
    {
        "name": "Weather",
        "prompt": (
            "Fetch the current temperature for Dubai from "
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=25.2048&longitude=55.2708"
            "&current=temperature_2m&temperature_unit=celsius "
            "and return ONLY the temperature number and unit, e.g. '34°C'."
        ),
    },
    {
        "name": "Tutorial Count",
        "prompt": (
            "Count how many README.md files exist under the tutorial/ "
            "directory. Return ONLY the count as a number."
        ),
    },
    {
        "name": "Repo Summary",
        "prompt": (
            "Read the first 30 lines of README.md and return a one-sentence "
            "summary of what this repository is about."
        ),
    },
]


def run_one_task(task: dict) -> dict:
    """Run a single task and return timing + result."""
    start = time.time()
    try:
        result = claude(
            task["prompt"],
            max_turns=5,
            max_budget_usd=0.10,
        )
        return {
            "name": task["name"],
            "result": result,
            "elapsed": round(time.time() - start, 1),
            "error": None,
        }
    except Exception as e:
        return {
            "name": task["name"],
            "result": None,
            "elapsed": round(time.time() - start, 1),
            "error": str(e),
        }


def demo_parallel():
    """Run multiple Claude invocations concurrently."""
    print("=" * 60)
    print("DEMO 3: Parallel Agents")
    print("=" * 60)
    print(f"Launching {len(PARALLEL_TASKS)} tasks in parallel...\n")

    overall_start = time.time()

    with ThreadPoolExecutor(max_workers=len(PARALLEL_TASKS)) as pool:
        futures = {
            pool.submit(run_one_task, task): task["name"]
            for task in PARALLEL_TASKS
        }
        for future in as_completed(futures):
            r = future.result()
            status = "OK" if r["error"] is None else f"ERR: {r['error']}"
            print(f"  [{r['elapsed']:>5}s] {r['name']}: {status}")
            if r["result"]:
                # Indent multi-line results
                for line in r["result"].splitlines():
                    print(f"          {line}")
            print()

    total = round(time.time() - overall_start, 1)
    print(f"All tasks completed in {total}s (parallel)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

DEMOS = {
    "simple": demo_simple,
    "structured": demo_structured,
    "parallel": demo_parallel,
}


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Python Orchestrator — demo scripts"
    )
    parser.add_argument(
        "--demo",
        choices=list(DEMOS.keys()),
        help="Run a specific demo (default: all)",
    )
    args = parser.parse_args()

    # Preflight check
    check = subprocess.run(
        ["claude", "--version"], capture_output=True, text=True
    )
    if check.returncode != 0:
        print("Error: `claude` CLI not found. Install with: brew install --cask claude-code")
        sys.exit(1)
    print(f"Claude Code version: {check.stdout.strip()}\n")

    if args.demo:
        DEMOS[args.demo]()
    else:
        for demo_fn in DEMOS.values():
            demo_fn()


if __name__ == "__main__":
    main()
