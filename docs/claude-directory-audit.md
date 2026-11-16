# Claude directory audit: 1.0.1

The directory refused 1.0.0 at commit `4053a6b` because an unverified
organization's submission must use fields Claude Code reads and the directory's
remote-MCP/package.json allow-lists. The only offending field in the Claude
configuration was `mcpServers.freckle.extensions` in `freckle-mcp/.mcp.json`.

## Sources and scope

Checked on November 16, 2026 against:

- [Claude plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
- [Claude marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference)
- [Claude MCP reference](https://code.claude.com/docs/en/mcp)
- The directory rejection's explicit remote-MCP and package.json allow-lists.

The Claude marketplace points to `./freckle-mcp`. Its manifest names an MCP
file and `./skills/`. Claude also automatically reads a plugin-root `.mcp.json`
before its manifest's declared MCP files; adding a clean file alone would leave
the OpenAI extension in that automatic load path.

## Field-by-field audit

Paths below are JSON property paths. Array indexes identify the existing entry.

| File | Field | Result |
| --- | --- | --- |
| `.claude-plugin/marketplace.json` | `name` | Documented marketplace identifier; keep. |
| Same | `owner` | Documented maintainer object; keep. |
| Same | `owner.name` | Documented required maintainer name; keep. |
| Same | `metadata` | Documented container for marketplace description/version/pluginRoot; keep. |
| Same | `metadata.description` | Documented alternate location for the marketplace description; keep. This is not a free-form plugin-entry metadata field. |
| Same | `plugins` | Documented plugin-entry array; keep. |
| Same | `plugins[0].name` | Documented plugin identifier; keep. |
| Same | `plugins[0].source` | Documented relative plugin source; keep `./freckle-mcp`. |
| Same | `plugins[0].description` | Documented entry description; keep. |
| `freckle-mcp/.claude-plugin/plugin.json` | `name` | Documented plugin identifier; keep. |
| Same | `description` | Documented plugin description; keep. |
| Same | `version` | Documented plugin version; bump from `1.0.0` to `1.0.1`. |
| Same | `author` | Documented author object; keep. |
| Same | `author.name` | Documented required author name; keep. |
| Same | `author.email` | Documented optional author email; keep. |
| Same | `author.url` | Documented optional author URL; keep. |
| Same | `homepage` | Documented URL; keep. |
| Same | `repository` | Documented source URL; keep. |
| Same | `license` | Documented license identifier; keep. |
| Same | `keywords` | Documented array of strings; keep. |
| Same | `mcpServers` | Documented plugin-relative JSON config path; change to `./.claude-plugin/mcp.json`. |
| Same | `skills` | Documented plugin-relative skills directory; keep `./skills/`. |
| Old `freckle-mcp/.mcp.json`; new `freckle-mcp/.claude-plugin/mcp.json` | `mcpServers` | Documented server map wrapper; keep. |
| Same | `mcpServers.freckle` | Documented named server object; keep. |
| Same | `mcpServers.freckle.type` | Directory allow-list permits this; keep `"http"`. |
| Same | `mcpServers.freckle.url` | Directory allow-list permits this; keep `https://next-api.freckle.io/mcp/full`. |
| Old `freckle-mcp/.mcp.json` | `mcpServers.freckle.extensions` | Outside the remote-server allow-list; remove from Claude's load path. |
| Same | `mcpServers.freckle.extensions.com.openai` | OpenAI-only namespace under the unsupported extension; retain only for Codex/ChatGPT. |
| Same | `mcpServers.freckle.extensions.com.openai.auth` | OpenAI-only authentication extension; retain only for Codex/ChatGPT. |
| Same | `mcpServers.freckle.extensions.com.openai.auth.type` | OpenAI-only `"oauth"` value, not a Claude OAuth config; retain only for Codex/ChatGPT. |
| Same | `mcpServers.freckle.extensions.com.openai.auth.client` | OpenAI-only client configuration; retain only for Codex/ChatGPT. |
| Same | `mcpServers.freckle.extensions.com.openai.auth.client.mode` | OpenAI-only `"cimd"` value; retain only for Codex/ChatGPT. |
| Any `package.json` | All fields | No package.json exists anywhere in the repository. No package cleanup is needed. |

No other fields in these Claude-read JSON files are outside the documented
schemas or the applicable directory allow-list. The remote-server allow-list
does not replace the plugin or marketplace schemas.

Claude's new server has exactly `type` and `url`. No `oauth` object is needed:
Claude discovers the server's OAuth metadata, registers a client, and prompts
for authorization. No client ID was invented or copied from OpenAI.

## Compatibility and file changes

- Move the old root `.mcp.json`, byte for byte, to
  `freckle-mcp/.codex-plugin/mcp.json`; remove the root file so Claude cannot
  auto-load its OpenAI extension.
- Add `freckle-mcp/.claude-plugin/mcp.json` with only the HTTP type and URL.
- Update each client's manifest to reference its own MCP file and version
  `1.0.1`. Every other Codex manifest field is unchanged, including `interface`
  and all `extensions.com.openai` review and publication data.
- Leave `.agents/plugins/marketplace.json`, the Claude marketplace, skills,
  assets, and the publish workflow unchanged. Update README and OpenAI
  submission instructions for the new paths.

## Verification

Used Claude Code **2.1.318**:

```sh
claude plugin validate --json --strict .claude-plugin/marketplace.json
claude plugin validate --json --strict freckle-mcp
claude plugin validate --json --profile directory freckle-mcp
```

All three commands passed. The manifest checks reported no errors or warnings.
The separate directory findings contained an existing, nonblocking
`ICON_MISSING` warning and an informational `PRIVACY_URL_MISSING` finding
(privacy URL taken from the repository README). No hold or incomplete checks
were reported. The validator also passed the old configuration, so validation
alone does not prove compliance with the rejection's stricter allow-list.

Installed this checkout with a separate temporary `CLAUDE_CONFIG_DIR`, without
changing the user's normal Claude settings:

```sh
claude plugin marketplace add "$PWD" --json
claude plugin install freckle-mcp@freckle-mcp-plugins --json
claude plugin list --json
claude plugin details freckle-mcp@freckle-mcp-plugins
claude mcp list
claude mcp login --no-browser plugin:freckle-mcp:freckle
```

- Installation succeeded at version `1.0.1`. The loaded server config contained
  only `type` and `url`; the inventory showed two skills and one MCP server.
- The live server health check returned
  `plugin:freckle-mcp:freckle: https://next-api.freckle.io/mcp/full (HTTP) - ! Needs authentication`.
- In an interactive terminal, login discovered OAuth and generated an
  authorization URL at `https://clerk.freckle.io/oauth/authorize` with PKCE,
  client ID, resource and redirect parameters. Canceled at
  `Waiting for authorization`; no browser sign-in or tool calls were completed.
- Parsed all six repository JSON files as plain objects. Confirmed no
  package.json exists and the Claude server has exactly the required fields.
- Compared the moved Codex MCP file byte for byte with `4053a6b`; it is
  identical. Compared the Codex manifest structurally after excluding only
  `version` and `mcpServers`; it is identical. The agents marketplace is also
  byte-identical. A fresh Codex/ChatGPT OAuth session was not exercised.
- Ran the exact `Build zips` shell block from `publish-skills.yml` in a temporary
  directory. Both individual skill archives and the combined archive built;
  checked their skill contents and every SHA256SUMS entry. No release upload or
  tag push was run. The workflow still reads only `freckle-mcp/skills/`; its path
  filters mean this config/documentation-only PR will not trigger publishing.
- `git diff --check` passed.

The directory runs checks beyond the local validator. Actual directory
acceptance requires resubmission and a decision from Anthropic; it has not been
observed by this audit.
