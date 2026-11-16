# Claude directory audit: isolated 1.0.2 package

## Exact submission target

- **Repository:** `freckle-io/agent-plugins-mcp`
- **Plugin folder:** `claude/freckle-mcp`
- **Manifest:** `claude/freckle-mcp/.claude-plugin/plugin.json`
- **Version:** `1.0.2`

Submit that folder after this PR lands. Do not submit the repository root or
`freckle-mcp/`: those contain repository tooling and Codex/ChatGPT packaging.
The root Claude marketplace now points to `./claude/freckle-mcp`, so the existing
marketplace/install commands continue to work.

```text
claude/freckle-mcp/
├── .claude-plugin/
│   ├── plugin.json
│   └── icon.png
├── .mcp.json
├── LICENSE
├── README.md
└── skills/
    ├── freckle-plan/SKILL.md
    └── freckle/
        ├── SKILL.md
        ├── ADS.md
        ├── BUILD.md
        ├── LIST.md
        └── SIGNALS.md
```

## Why 1.0.1 was still rejected

The resubmission after PR #2 merged at `7648af8` reported files outside the
unverified-organization allow-list and an incompletely readable plugin.
The previous package still contained:

| Old path | Problem | Resolution |
| --- | --- | --- |
| `freckle-mcp/.claude-plugin/mcp.json` | Inside `.claude-plugin`, only plugin.json, images and a constrained marketplace.json are allowed. | Move the clean config to the new package's root `.mcp.json`. |
| `freckle-mcp/.codex-plugin/plugin.json` | Another client's plugin packaging is in the submitted folder. | Leave it in the Codex package, outside the new Claude folder. |
| `freckle-mcp/.codex-plugin/mcp.json` | Codex-only configuration is in the submitted folder. | Leave it outside the new Claude folder, preserving OAuth CIMD. |
| `freckle-mcp/assets/freckle-light.png` | The image is allowed, but the directory validator does not recognize its filename as the default icon. | Copy the existing 520×520 image to `.claude-plugin/icon.png`. |
| `freckle-mcp/` | It has no local README or license; earlier validation used the repository README. | Give the isolated folder its own README and a byte-identical license copy. |

Before this change, `claude plugin validate --strict --profile directory
freckle-mcp` exited 1 for `ICON_MISSING` and also named `PRIVACY_URL_MISSING`.
The new manifest explicitly sets the documented `privacyPolicyUrl`, and the
recognized icon removes the warning. The new folder also validates when copied
outside this git repository, proving it does not depend on parent files.

## Reproducible inventory

The complete script is [scripts/audit_claude_directory.py](../scripts/audit_claude_directory.py).
It uses `git ls-files --stage -z` and reads every tracked worktree file; stage
new files before running it. `--ref` instead audits the committed blobs at a
specified git ref. It rejects untracked files inside the submitted folder, so
a successful run cannot silently omit a local extra file there.

```sh
python3 scripts/audit_claude_directory.py
# Historical comparison (expected to fail):
python3 scripts/audit_claude_directory.py --ref 7648af8 --plugin freckle-mcp
```

The guard checks regular files (no symlinks/submodules), ASCII-safe path names,
allowed extensions and special filenames, shebangs, UTF-8 and NUL bytes in
text, package-manager configs, other-client/nested Claude packaging,
`.claude/skills`, restricted `.claude-plugin` contents and marketplace sources,
JSON/YAML in egress, Markdown-only commands/agents, skill-folder structure,
output-styles, and the JSON fields used by this package. New hooks/LSP/monitor
or package.json configs fail closed until their schema checks are added.
The checks for required package files, matching license/icon and identical
skill copies are additional repository packaging checks.

The script is intentionally a guard for this repository, not a replacement for
Claude's full schema validator. CI runs both. The excluded `.py` audit script is
repository tooling and is deliberately outside the submitted folder.

`SUBMIT` rows are checked relative to `claude/freckle-mcp`. `EXCLUDE` rows are
outside that folder; their rule results describe their repository paths and do
not contribute to submission failures. This covers every tracked file, including
files that must remain outside the submission.

| Tracked file | Submission scope | File-rule result |
| --- | --- | --- |
| `.agents/plugins/marketplace.json` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `.claude-plugin/marketplace.json` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `.github/workflows/publish-skills.yml` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `.github/workflows/validate-plugins.yml` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `LICENSE` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `README.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `assets/freckle.png` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/.claude-plugin/icon.png` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/.claude-plugin/plugin.json` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/.mcp.json` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/LICENSE` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/README.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/skills/freckle-plan/SKILL.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/skills/freckle/ADS.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/skills/freckle/BUILD.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/skills/freckle/LIST.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/skills/freckle/SIGNALS.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `claude/freckle-mcp/skills/freckle/SKILL.md` | SUBMIT | allowed type/path; UTF-8 without NUL where text |
| `docs/claude-directory-audit.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `docs/openai-submission.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/.codex-plugin/mcp.json` | EXCLUDE | other client's plugin packaging |
| `freckle-mcp/.codex-plugin/plugin.json` | EXCLUDE | other client's plugin packaging |
| `freckle-mcp/assets/freckle-dark.png` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/assets/freckle-light.png` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/skills/freckle-plan/SKILL.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/skills/freckle/ADS.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/skills/freckle/BUILD.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/skills/freckle/LIST.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/skills/freckle/SIGNALS.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `freckle-mcp/skills/freckle/SKILL.md` | EXCLUDE | allowed type/path; UTF-8 without NUL where text |
| `scripts/audit_claude_directory.py` | EXCLUDE | file type outside allow-list |

Inventory: 31 tracked files; 11 submitted; 20 excluded; 0 submission violations.

## Rule coverage and config fields

- All 11 submitted files are ordinary files: 6 skill Markdown files, a README,
  LICENSE, 2 JSON objects and one PNG. The PNG is the existing Freckle logo,
  byte-identical to `freckle-mcp/assets/freckle-light.png`.
- No submitted file has a shebang, odd path characters, non-UTF-8 text or NUL in
  text. No package-manager config, `.claude/skills`, other plugin, nested
  `.claude-plugin`, egress config, commands/agents, hooks/LSP/monitor config,
  output-styles or package.json is present.
- `.claude-plugin` contains exactly `plugin.json` and `icon.png`.
- Each of the two `skills/` subfolders has its own `SKILL.md`; all six files
  match the existing Codex/source skill files byte for byte.

| Config | Fields | Schema disposition |
| --- | --- | --- |
| Claude plugin.json | `name`, `description`, `version`, `homepage`, `repository`, `license`, `keywords`, `skills`, `mcpServers` | Documented plugin fields; version is now 1.0.2 and MCP path is `./.mcp.json`. |
| Claude plugin.json author | `name`, `email`, `url` | All documented author fields; retained. |
| Claude plugin.json | `privacyPolicyUrl` | Documented directory-listing field recognized by the validator; added to clear its privacy finding. |
| Claude .mcp.json | `mcpServers.freckle.type`, `mcpServers.freckle.url` | Exactly `http` and `https://next-api.freckle.io/mcp/full`; no extensions or OAuth overrides. |
| Root Claude marketplace | `name`, `owner.name`, `metadata.description`, `plugins[].name`, `plugins[].source`, `plugins[].description` | Documented fields; only source changes to `./claude/freckle-mcp`. Outside the submitted folder. |

Sources: the resubmission's explicit file restrictions,
[Claude manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference),
[marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference),
and [MCP reference](https://code.claude.com/docs/en/mcp), checked November 16, 2026.

## Verification

Claude Code **2.1.318**:

```sh
claude plugin validate --json --strict --profile directory claude/freckle-mcp
claude plugin validate --json --strict .claude-plugin/marketplace.json
```

Both pass with **zero errors, warnings or directory findings**, no incomplete
checks and no parent-directory notes. The standalone copy also passes the same
strict directory profile with zero findings.

Using a new temporary `CLAUDE_CONFIG_DIR`:

```sh
claude plugin marketplace add "$PWD" --json
claude plugin install freckle-mcp@freckle-mcp-plugins --json
claude plugin list --json
claude plugin details freckle-mcp@freckle-mcp-plugins
claude mcp list
```

Installation succeeds at **1.0.2** from `claude/freckle-mcp`, and the inventory
shows **two skills and one MCP server**. Its loaded server has only `type` and
`url`. The live health check returns:

```text
plugin:freckle-mcp:freckle: https://next-api.freckle.io/mcp/full (HTTP) - ! Needs authentication
```

Browser sign-in and authenticated MCP tool calls were not run. This is local
validation and installation evidence, not a claim of directory acceptance.
Izak handles the resubmission.

Other checks:

- Exercised the audit's individual rejection rules with negative fixtures,
  including shebang, invalid UTF-8, NUL, forbidden paths/types, unknown manifest
  and remote-MCP fields, and an extra local marketplace plugin. Allowed skill
  paths and symlink rejection were also checked.
- Compared every remaining `freckle-mcp/` file and the agents marketplace with
  `7648af8`: **byte-identical**. Codex's manifest remains **1.0.1**, with its
  listing and review/publication extensions unchanged; its own release version
  is independent of Claude's 1.0.2. No Codex/ChatGPT login was run.
- Built and inspected the OpenAI upload ZIP. It contains `.codex-plugin` and the
  referenced MCP file with OAuth CIMD; it contains no Claude manifest/package.
- Ran the unchanged `publish-skills.yml` **Build zips** shell block in a temporary
  directory, verified combined archive contents and every SHA256SUMS entry. No
  release upload or tag mutation was run.
- `.github/workflows/validate-plugins.yml` now runs the inventory/skill-copy guard
  and both strict Claude validations on PRs and main, using pinned Claude Code
  2.1.318. It does not publish releases.
- `git diff --check` passes.

## Keeping skills in sync

`freckle-mcp/skills/` remains the source for the existing download/release
workflow and Codex package. Update the matching files under
`claude/freckle-mcp/skills/` in the same change. CI compares their exact file
sets and contents, so a missing copy, added file or edited skill cannot silently
drift between clients. The submitted folder uses real files, without symlinks or
paths outside its root.
