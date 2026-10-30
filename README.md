<p align="center">
  <a href="https://freckle.io">
    <img src="./assets/freckle.png" alt="Freckle" height="72">
  </a>
</p>

<p align="center">
  <strong>Use Freckle from any AI agent over MCP</strong> — the Freckle MCP server plus
  the skills that teach your agent to use it. No CLI required.
</p>

<p align="center">
  <a href="https://freckle.io">freckle.io</a> · MCP server: <code>https://next-api.freckle.io/mcp/full</code>
</p>

Freckle is an AI-powered lead enrichment platform: build lists of companies and
people, enrich and score them, import CRM records, watch Signals and push Ads
audiences, all from natural language. This repo packages Freckle's MCP server
and its skills for Claude Code, Codex, Claude Desktop, claude.ai and any other
MCP client.

Prefer the `freckle` CLI? Use [freckle-io/agent-plugins](https://github.com/freckle-io/agent-plugins)
instead. Install one or the other: both ship a skill named `freckle`.

## Claude Code

Install the plugin. It connects the MCP server and adds the skills in one step:

```
/plugin marketplace add freckle-io/agent-plugins-mcp
/plugin install freckle-mcp@freckle-mcp-plugins
```

Then run `/mcp`, pick **freckle**, sign in to Freckle in the browser and choose
your Workspace.

MCP server only, without the skills:

```bash
claude mcp add --transport http freckle https://next-api.freckle.io/mcp/full
```

## Codex

```bash
codex plugin marketplace add freckle-io/agent-plugins-mcp
```

Open Codex, run `/plugins`, install **Freckle MCP** and sign in when Codex asks.

MCP server only, without the skills:

```bash
codex mcp add freckle --url https://next-api.freckle.io/mcp/full
```

## Claude Desktop and claude.ai

1. **Connect the server.** Settings → Connectors → *Add custom connector*.
   Name it `Freckle`, paste `https://next-api.freckle.io/mcp/full`, then
   *Connect* and sign in to Freckle.
2. **Add the skills.** Download [`freckle.zip`][freckle-zip] and
   [`freckle-plan.zip`][plan-zip], then upload each one under Settings →
   Capabilities → Skills.

## Other MCP clients

Point any client that supports remote (streamable HTTP) MCP servers with OAuth
at:

```
https://next-api.freckle.io/mcp/full
```

For example, in Cursor's `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "freckle": { "url": "https://next-api.freckle.io/mcp/full" }
  }
}
```

Sign in when the client asks and choose your Workspace. Any member of a
Workspace can use it.

## Download the skills

The skills are in [`freckle-mcp/skills/`](./freckle-mcp/skills/) and are
published as zips on every change:

| Download | Contains |
| --- | --- |
| [`freckle-mcp-skills.zip`][all-zip] | Both skills, for `~/.claude/skills/` or `~/.codex/skills/` |
| [`freckle.zip`][freckle-zip] | `freckle`: the router for all Freckle work (lists, enrichment, workflows, CRM imports, Signals, Ads audiences, credits, connections) |
| [`freckle-plan.zip`][plan-zip] | `freckle-plan`: turns a call, notes or an idea into a build plan before anything runs |

To install them for Claude Code or Codex without the plugin:

```bash
mkdir -p ~/.claude/skills
curl -fsSL https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/freckle-mcp-skills.zip -o /tmp/freckle-mcp-skills.zip
unzip -o /tmp/freckle-mcp-skills.zip -d ~/.claude/skills
```

For Codex, unzip into `~/.codex/skills` instead. Checksums are in
[`SHA256SUMS`][sums].

## What's inside

- **`freckle-mcp/.mcp.json`**: the Freckle MCP server connection.
- **`freckle-mcp/skills/`**: the `freckle` and `freckle-plan` skills. They add
  the GTM judgment the tool descriptions don't carry: confirm the cost before
  spending credits, sample 10 rows before a big run, report real outcomes.
- **`freckle-mcp/.claude-plugin/`, `freckle-mcp/.codex-plugin/`**: plugin
  manifests for Claude Code and Codex.

The plugin ships no binaries, hooks or secrets. Sign-in goes through your
client's OAuth flow, and integration secrets go only through the browser form
the `connections_setup` tool returns.

---

<p align="center">
  <a href="https://freckle.io">Website</a> ·
  <a href="https://freckle.io/privacy-policy">Privacy policy</a> ·
  <a href="https://freckle.io/terms-of-service">Terms of service</a>
</p>

[all-zip]: https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/freckle-mcp-skills.zip
[freckle-zip]: https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/freckle.zip
[plan-zip]: https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/freckle-plan.zip
[sums]: https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/SHA256SUMS
