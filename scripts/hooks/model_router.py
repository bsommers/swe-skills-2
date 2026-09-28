#!/usr/bin/env python3
"""Adaptive model router hook for Antigravity and agentic workflows.

Inspects tool calls and session prompts dynamically to route tasks to the most
cost-effective model tier (flash_lite, flash, pro) to conserve tokens:

  pretooluse    PreToolUse (agy) — intercepts `invoke_subagent` calls. Evaluates
                prompt and role complexity, injecting `overwrite: {"Model": <tier>}`.
  preinvocation PreInvocation (agy) — evaluates prompt density and token demand,
                optionally injecting ephemeral routing advice.
  evaluate      CLI / testing — evaluates a text description and outputs the
                recommended tier and rationale as JSON.

Configuration (all optional, env vars):
  SWE_SKILLS_MODEL_ROUTER_ENABLED      1 = active, 0 = no-op pass-through (default 1)
  SWE_SKILLS_MODEL_ROUTER_DEFAULT_TIER fallback tier (default "flash")
  SWE_SKILLS_MODEL_ROUTER_DEBUG        1 = print debug info to stderr (default 0)

A hook that fails must never break the session: unexpected errors exit 0 silently.
"""
import json
import os
import re
import sys

DEFAULT_TIER = os.environ.get("SWE_SKILLS_MODEL_ROUTER_DEFAULT_TIER", "flash")

HIGH_COMPLEXITY_PATTERNS = [
    r"\barchitect\w*\b",
    r"\brefactor\w*\b",
    r"\bsecur\w*\b",
    r"\baudit\w*\b",
    r"\bvulnerab\w*\b",
    r"\bconcurr\w*\b",
    r"\brace\s+condition\b",
    r"\bdeadlock\b",
    r"\bmemory\s+leak\b",
    r"\bdeep\s+debug\w*\b",
    r"\broot\s+cause\b",
    r"\bdiff\s+review\b",
    r"\badversarial\b",
    r"\binvariant\w*\b",
    r"\bthreat\s+model\w*\b",
    r"\bcrypto\w*\b",
    r"\bauth\w*\b",
]

LOW_COMPLEXITY_PATTERNS = [
    r"\blint\b",
    r"\bformat\w*\b",
    r"\btypo\w*\b",
    r"\bboilerplate\b",
    r"\bmechanical\b",
    r"\bgrep\b",
    r"\bsurvey\b",
    r"\blist\s+files\b",
    r"\bdoc(?:s|umentation)?\s+sync\b",
    r"\breadme\b",
    r"\bchangelog\b",
]


def is_enabled():
    return os.environ.get("SWE_SKILLS_MODEL_ROUTER_ENABLED", "1").strip().lower() not in (
        "0",
        "false",
        "no",
        "",
    )


def log_debug(msg):
    if os.environ.get("SWE_SKILLS_MODEL_ROUTER_DEBUG", "0").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        print(f"[model_router] {msg}", file=sys.stderr)


def evaluate_task(role, prompt, file_paths=None):
    """Determine recommended model tier ('pro', 'flash', 'flash_lite') based on signals."""
    corpus = f"{role} {prompt} {' '.join(file_paths or [])}".lower()

    # Check high-complexity signals first
    for pattern in HIGH_COMPLEXITY_PATTERNS:
        if re.search(pattern, corpus):
            return "pro", f"Matched high-complexity pattern: {pattern}"

    # Check file path sensitivity
    for path in file_paths or []:
        if re.search(r"(?:auth|crypto|session|permission|migration|types/)", path.lower()):
            return "pro", f"Sensitive subsystem target: {path}"

    # Check low-complexity signals
    for pattern in LOW_COMPLEXITY_PATTERNS:
        if re.search(pattern, corpus):
            return "flash_lite", f"Matched low-complexity pattern: {pattern}"

    return DEFAULT_TIER, "Standard complexity baseline"


def handle_pretooluse(payload):
    """Handle PreToolUse event. Overwrites Model argument on invoke_subagent if needed."""
    if not is_enabled():
        return {"decision": "allow"}

    tool_call = payload.get("toolCall", {})
    name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    if name != "invoke_subagent":
        return {"decision": "allow"}

    subagents = args.get("Subagents", [])
    if not subagents or not isinstance(subagents, list):
        return {"decision": "allow"}

    modified = False
    new_subagents = []

    for agent in subagents:
        role = agent.get("Role", "")
        prompt = agent.get("Prompt", "")
        current_model = agent.get("Model", "inherit")

        recommended_tier, reason = evaluate_task(role, prompt)
        log_debug(f"Agent '{role}': current={current_model}, recommended={recommended_tier} ({reason})")

        # Overwrite if current model is inherit or differs from recommended tier
        if current_model in ("inherit", "") or (current_model != recommended_tier and current_model != "pro"):
            new_agent = dict(agent)
            new_agent["Model"] = recommended_tier
            new_subagents.append(new_agent)
            modified = True
        else:
            new_subagents.append(agent)

    if modified:
        return {
            "decision": "allow",
            "overwrite": {
                "Subagents": new_subagents
            },
        }

    return {"decision": "allow"}


def handle_preinvocation(payload):
    """Handle PreInvocation event. Injects ephemeral hints when high density is detected."""
    if not is_enabled():
        return {}

    user_prompt = payload.get("userPrompt", "")
    if not user_prompt:
        return {}

    tier, reason = evaluate_task("User Prompt", user_prompt)
    if tier == "pro":
        log_debug(f"PreInvocation detected high-complexity prompt ({reason})")
        return {
            "injectSteps": [
                {
                    "ephemeralMessage": (
                        "Adaptive Model Router: Complex architecture or review task detected. "
                        "Delegate heavy reasoning slices to a 'pro' subagent to conserve main session tokens."
                    )
                }
            ]
        }

    return {}


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "evaluate"

    try:
        raw_in = sys.stdin.read().strip()
        payload = json.loads(raw_in) if raw_in else {}
    except Exception as e:
        log_debug(f"Failed to parse stdin JSON: {e}")
        payload = {}

    try:
        if mode in ("pretooluse", "pre_tool_use"):
            res = handle_pretooluse(payload)
            print(json.dumps(res))
        elif mode in ("preinvocation", "pre_invocation"):
            res = handle_preinvocation(payload)
            print(json.dumps(res))
        elif mode == "evaluate":
            role = payload.get("role", "")
            prompt = payload.get("prompt", raw_in)
            files = payload.get("files", [])
            tier, reason = evaluate_task(role, prompt, files)
            print(json.dumps({"tier": tier, "reason": reason}))
        else:
            print(json.dumps({"decision": "allow"}))
    except Exception as e:
        log_debug(f"Unexpected handler error: {e}")
        print(json.dumps({"decision": "allow"}))

    return 0


if __name__ == "__main__":
    sys.exit(main())
