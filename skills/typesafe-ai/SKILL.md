---
name: typesafe-ai
description: Use when building, reviewing, or debugging code that calls TypeSafe; when writing its questions or state; when replacing an LLM prompt-and-parse step, keyword matching, or a brittle heuristic with a typed question; or when brainstorming where programmable common sense fits in an app.
---

# Build with TypeSafe

TypeSafe's **Jev**, the first public **System One model**, answers typed questions about state your
application supplies. State is the text, images, and application data your code sends with a
request. Jev can answer a Choice among options, a Noul (the probability that a statement is true), a
Score on levels you describe, or a Box that locates something in an image. Each answer comes back as
typed data with calibrated probabilities, for your code to use.

The rest of this skill is guidance: patterns that tend to produce reliable integrations. None of it
is absolute. Models change, applications differ, and edge cases exist. When a situation calls for
something else, test the alternative and use your judgment.

## Judgments from Jev, decisions in code

Integrations tend to work best when Jev makes the judgments and code decides what to do with
them. Think of each decision as a **truth table**. Jev supplies the inputs, such as "Does the
customer sound frustrated?" or "Which product is the message about?". Code holds the logic that
maps those inputs to an action.

A question that asks Jev to make the decision, such as "Should this ticket be escalated?" or "What
should the agent do next?", usually means the question is at the wrong layer. Instead, break the
decision into the judgments it depends on, and write the decision itself in code, where it's
visible and testable. Writing out the table often shows gaps in the business logic too. A
combination of judgments with no defined outcome is a design question about the system, and it is
best settled in code.

## Live docs

The live docs are the source of truth for request syntax, SDKs, question types, limits, and current model behavior:
- Documentation index: [https://docs.typesafe.ai/llms.txt](https://docs.typesafe.ai/llms.txt)
- Schemas & API reference: [OpenAPI spec](https://api.typesafe.ai/openapi.json) and [HTTP API](https://docs.typesafe.ai/go/api.md)
- Primitives & question types: [primitives](https://docs.typesafe.ai/go/primitives.md) and [images](https://docs.typesafe.ai/go/images.md)
- Architecture & cookbooks: [how to build](https://docs.typesafe.ai/go/how-to-build.md) and [patterns](https://docs.typesafe.ai/go/patterns.md)

## Workflow

1. **Start from decision logic**: Sketch the truth table mapping judgments to code actions. Arithmetic, policy, and exact lookups belong in code; language and image understanding belong in Jev.
2. **Keep question definitions centralized**: Maintain questions, criteria, and probability thresholds in a dedicated module for auditability.
3. **Probe live API**: Test representative, hard, and negative edge cases.
4. **Integrate**: Log payloads, fail visibly, and set timeouts/retries.

## Design the state

State is the context your application sends to Jev (text, JSON, images, documents).
- **Include what a human needs**: If a human grader could not decide from the state, neither can Jev.
- **Keep it compact**: Omit irrelevant fields and metadata that clutter the context.
- **Images as assets**: Pass images via the  map ( or ) and reference their keys in state, instructions, or criteria.
See [state-requests-and-answers.md](references/state-requests-and-answers.md) for detailed state shaping and asset structuring.

## Write the questions

Questions define the judgments Jev makes over your state. Pick the primitive that fits the judgment:
- **Choice**: Pick one option from a fixed list or candidates supplied in state. Calibrated probabilities across options.
- **Noul**: Probability (0 to 1) that a statement about the state is true. Use for boolean conditions and filters.
- **Score**: Map an aspect onto an ordered scale (e.g. 1-5, rubrics).
- **Box**: Locate an object in an image ( normalized 0-1). Requires Jev 1.14+ and .

Detailed question authoring patterns, criteria formatting, and advanced structures are documented in [questions-and-criteria.md](references/questions-and-criteria.md).

## Compose requests

Batch multiple related questions into a single request over the same state to minimize latency and cost.
- Questions are evaluated independently against the shared state.
- Send the  header whenever images or  questions are included.
See [state-requests-and-answers.md](references/state-requests-and-answers.md) for batch composition patterns.

## Read the answers

Jev returns typed outputs with calibrated probabilities:
- **Noul**: Read  (0.0 to 1.0). Use threshold bands (e.g. >0.7 yes, <0.3 no; middle band handles uncertain/manual review).
- **Choice**: Read the probability distribution across . Pick the top option or gate on margin.
- **Score**: Inspect the level distribution in addition to  to catch bimodal evaluations.
- **Box**: Read  normalized coordinates  (0-1) and scale by image dimensions.
See [state-requests-and-answers.md](references/state-requests-and-answers.md) for calibration and probability handling.

## Test with the live API

Probe questions against real data using your . Check the sent payload, state completeness, candidate lists, and question scope before tuning wording. Avoid prompt gymnastics (caveats, overfitting thresholds).

Guidance on live testing, diagnosing wrong answers, yellow flags, and architectural cookbooks (function calling, value extraction, RAG re-ranking) is documented in [testing-and-cookbooks.md](references/testing-and-cookbooks.md).
