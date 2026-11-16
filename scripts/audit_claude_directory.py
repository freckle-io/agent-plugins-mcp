"""Inventory tracked files against Freckle's unverified-directory rejection rules.

This is a repository-specific file/field guard, not a general Claude schema.
Run Claude's strict directory validator as well for complete schema validation.
"""

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "claude/freckle-mcp"
TEXT = {".md", ".txt", ".text", ".json", ".yaml", ".yml"}
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
PACKAGE_CONFIGS = {
    "pnpm-workspace.yaml", "pnpm-workspace.yml", "pnpm-lock.yaml",
    "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "bun.lock",
    "bun.lockb", ".npmrc", ".yarnrc", ".yarnrc.yml", ".pnpmfile.cjs",
}
MANIFEST_FIELDS = {
    "name", "version", "description", "author", "homepage", "repository",
    "license", "keywords", "mcpServers", "skills", "privacyPolicyUrl",
}
SERVER_FIELDS = {
    "type", "url", "headers", "timeout", "alwaysLoad", "oauth", "name",
    "title", "displayName", "description",
}
OAUTH_FIELDS = {"clientId", "callbackPort", "authServerMetadataUrl", "scopes"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def files_at(ref):
    records = git("ls-tree", "-rz", ref) if ref else git("ls-files", "--stage", "-z")
    files = {}
    for record in records.split(b"\0"):
        if not record:
            continue
        meta, name = record.split(b"\t", 1)
        mode, second, third = meta.decode().split()
        if not ref and third != "0":
            raise ValueError("Resolve index conflicts before auditing")
        name = name.decode("utf-8")
        blob = git("cat-file", "blob", third) if ref and second == "blob" else None
        if not ref:
            path = ROOT / name
            blob = path.read_bytes() if path.is_file() and not path.is_symlink() else None
        files[name] = (mode, blob)
    return files


def problems(name, mode, data):
    path = PurePosixPath(name)
    parts = path.parts
    suffix = path.suffix.lower()
    errors = []
    if mode not in {"100644", "100755"} or data is None:
        return ["not a regular readable file (symlink/submodule/missing)"]
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", name):
        errors.append("odd path characters")
    if suffix not in TEXT | IMAGES and path.name not in {"LICENSE", "README", ".gitignore"}:
        errors.append("file type outside allow-list")
    if data.startswith(b"#!"):
        errors.append("starts with #!")
    if suffix not in IMAGES:
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append("text is not UTF-8")
        if b"\0" in data:
            errors.append("NUL in text")
    if path.name in PACKAGE_CONFIGS:
        errors.append("package-manager config/lockfile")
    if ".codex-plugin" in parts:
        errors.append("other client's plugin packaging")
    if any(parts[i:i + 2] == (".claude", "skills") for i in range(len(parts) - 1)):
        errors.append(".claude/skills")
    if ".claude-plugin" in parts:
        if parts[0] != ".claude-plugin" or len(parts) != 2:
            errors.append("another plugin's .claude-plugin directory")
        elif path.name not in {"plugin.json", "marketplace.json"} and suffix not in IMAGES:
            errors.append("file forbidden inside .claude-plugin")
    if "egress" in parts[:-1] and suffix in {".json", ".yaml", ".yml"}:
        errors.append("JSON/YAML in egress")
    if any(p in {"commands", "agents"} for p in parts[:-1]) and suffix != ".md":
        errors.append("commands/agents must be Markdown")
    if "output-styles" in parts[:-1]:
        errors.append("output-styles is forbidden")
    if parts[0] == "skills" and len(parts) < 3:
        errors.append("skills must have one directory per skill")
    if suffix == ".json":
        try:
            obj = json.loads(data)
            if not isinstance(obj, dict):
                errors.append("JSON must be a plain object")
            elif name == ".claude-plugin/plugin.json":
                unknown = obj.keys() - MANIFEST_FIELDS
                if unknown:
                    errors.append("manifest fields outside this package's documented schema: " + ", ".join(sorted(unknown)))
                if isinstance(obj.get("author"), dict) and obj["author"].keys() - {"name", "email", "url"}:
                    errors.append("unknown author fields")
            elif name == ".mcp.json":
                if obj.keys() != {"mcpServers"} or not isinstance(obj.get("mcpServers"), dict):
                    errors.append("expected mcpServers object")
                else:
                    for server in obj["mcpServers"].values():
                        if not isinstance(server, dict) or server.keys() - SERVER_FIELDS:
                            errors.append("unknown remote MCP fields")
                        elif isinstance(server.get("oauth"), dict) and server["oauth"].keys() - OAUTH_FIELDS:
                            errors.append("unknown OAuth fields")
            elif name == ".claude-plugin/marketplace.json":
                for entry in obj.get("plugins", []):
                    source = entry.get("source")
                    external = isinstance(source, dict) and source.get("source") in {"github", "git", "url"}
                    this_plugin = entry.get("name") == "freckle-mcp" and isinstance(source, str) and source in {".", "./", "./" + PLUGIN}
                    if not external and not this_plugin:
                        errors.append("marketplace may list only external repos or this plugin")
            elif path.name in {"hooks.json", ".lsp.json", "monitors.json", "package.json"}:
                errors.append("new config requires an explicit schema check in this repo's guard")
        except (ValueError, TypeError, AttributeError):
            errors.append("invalid JSON/config shape")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", help="Audit tracked blobs at a git ref instead of the worktree")
    parser.add_argument("--plugin", default=PLUGIN, help="Submitted folder, relative to repository root")
    args = parser.parse_args()
    files = files_at(args.ref)
    prefix = args.plugin.rstrip("/") + "/"
    submitted = {name[len(prefix):]: value for name, value in files.items() if name.startswith(prefix)}
    failures = []
    print("| Tracked file | Submission scope | File-rule result |")
    print("| --- | --- | --- |")
    for name, (mode, data) in sorted(files.items()):
        included = name.startswith(prefix)
        relative = name[len(prefix):] if included else name
        errors = problems(relative, mode, data)
        if included:
            failures.extend(name + ": " + error for error in errors)
        result = "; ".join(errors) if errors else "allowed type/path; UTF-8 without NUL where text"
        print(f"| `{name}` | {'SUBMIT' if included else 'EXCLUDE'} | {result} |")
    for required in [".claude-plugin/plugin.json", ".mcp.json", "README.md", "LICENSE"]:
        if required not in submitted:
            failures.append("missing tracked submission file: " + required)
    for name in submitted:
        parts = PurePosixPath(name).parts
        if parts[0] == "skills" and len(parts) >= 3 and f"skills/{parts[1]}/SKILL.md" not in submitted:
            failures.append("skill missing SKILL.md: " + parts[1])
    if not args.ref and args.plugin == PLUGIN:
        for path in (ROOT / args.plugin).rglob("*"):
            if (path.is_file() or path.is_symlink()) and path.relative_to(ROOT).as_posix() not in files:
                failures.append("untracked file in submitted folder: " + str(path.relative_to(ROOT)))
        source = {n.removeprefix("freckle-mcp/"): data for n, (_, data) in files.items() if n.startswith("freckle-mcp/skills/")}
        target = {n: data for n, (_, data) in submitted.items() if n.startswith("skills/")}
        if source != target:
            failures.append("Claude skill copies differ from freckle-mcp/skills; update both copies")
        if files.get("LICENSE", (None, None))[1] != submitted.get("LICENSE", (None, None))[1]:
            failures.append("Claude LICENSE differs from repository LICENSE")
        if files.get("freckle-mcp/assets/freckle-light.png", (None, None))[1] != submitted.get(".claude-plugin/icon.png", (None, None))[1]:
            failures.append("Claude icon differs from the existing Freckle logo")
    print(f"\nInventory: {len(files)} tracked files; {len(submitted)} submitted; {len(files) - len(submitted)} excluded; {len(failures)} submission violations.")
    for failure in failures:
        print("FAIL: " + failure)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
