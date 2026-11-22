#!/usr/bin/env python3
"""Validate a pr-review/v1 reply file. Stdlib only.

Usage: validate_pr_review.py REPLY.md [--schema SCHEMA.json]
Reads the last fenced block labelled `json pr-review/v1`, checks it against the
JSON Schema subset used here, then applies consistency rules. Exit 0 = valid.
"""
import json
import re
import sys
from pathlib import Path

DEFAULT_SCHEMA = Path(__file__).resolve().parent.parent / "references" / "pr-review-v1.schema.json"
FENCE = re.compile(r"^```json[ \t]+pr-review/v1[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}


def type_ok(value, name):
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, TYPES[name])


def check(value, schema, path, errs):
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path}: must be {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: {value!r} not in {schema['enum']}")
    if "type" in schema:
        names = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(type_ok(value, n) for n in names):
            errs.append(f"{path}: expected {'/'.join(names)}, got {type(value).__name__}")
            return
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errs.append(f"{path}: too short")
        if len(value) > schema.get("maxLength", 10**9):
            errs.append(f"{path}: longer than {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, int) and not isinstance(value, bool) and value < schema.get("minimum", value):
        errs.append(f"{path}: below minimum {schema['minimum']}")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errs.append(f"{path}: missing required '{key}'")
        for key, sub in value.items():
            if key in props:
                check(sub, props[key], f"{path}.{key}", errs)
            elif schema.get("additionalProperties") is False:
                errs.append(f"{path}: unknown property '{key}'")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errs.append(f"{path}: needs at least {schema['minItems']} items")
        for i, item in enumerate(value):
            if "items" in schema:
                check(item, schema["items"], f"{path}[{i}]", errs)


def consistency(doc, errs):
    findings = doc.get("findings", [])
    ids = [f.get("id") for f in findings if isinstance(f, dict)] + [q.get("id") for q in doc.get("questions", []) if isinstance(q, dict)]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errs.append(f"duplicate id {dup}")
    blocking = [f for f in findings if isinstance(f, dict) and f.get("blocking") is True]
    verdict = doc.get("verdict")
    if verdict == "approve" and blocking:
        errs.append("verdict approve but blocking findings exist")
    if verdict == "changes_requested" and not blocking:
        errs.append("verdict changes_requested needs at least one blocking finding")
    if verdict == "needs_info" and not doc.get("questions"):
        errs.append("verdict needs_info needs at least one question")
    for f in findings:
        if isinstance(f, dict) and f.get("severity") in ("critical", "high") and f.get("blocking") is False:
            errs.append(f"{f.get('id')}: {f['severity']} finding must be blocking")


def validate_text(text, schema_path=DEFAULT_SCHEMA):
    blocks = FENCE.findall(text)
    if not blocks:
        return ["no fenced block labelled 'json pr-review/v1'"]
    try:
        doc = json.loads(blocks[-1])
    except json.JSONDecodeError as exc:
        return [f"block is not valid JSON: {exc}"]
    errs = []
    check(doc, json.loads(Path(schema_path).read_text(encoding="utf-8")), "$", errs)
    if isinstance(doc, dict):
        consistency(doc, errs)
    return errs


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    schema = DEFAULT_SCHEMA
    if "--schema" in argv:
        i = argv.index("--schema")
        schema = Path(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    errs = validate_text(Path(argv[0]).read_text(encoding="utf-8"), schema)
    for e in errs:
        print(f"FAIL {e}")
    if not errs:
        print("OK pr-review/v1")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
