# Freckle for Claude Code

Build company and people lists, enrich leads, run Workflows, import CRM records,
monitor Signals and sync Ads audiences through Freckle's hosted MCP server.

## Install

```text
/plugin marketplace add freckle-io/agent-plugins-mcp
/plugin install freckle@freckle-mcp-plugins
```

Run `/mcp`, select **freckle**, sign in to Freckle and choose your Workspace.
The HTTP server at `https://next-api.freckle.io/mcp/full` provides OAuth discovery;
no client ID or credentials are shipped in this plugin.

The plugin includes the `freckle` and `freckle-plan` skills. Enrichment and list
runs can spend your Workspace's Freckle credits; the skills require a cost quote
and your approval before spending them. Buying credits and deleting accounts
are not exposed by the plugin.

## Directory submission

Submit repository `freckle-io/agent-plugins-mcp`, plugin folder
`claude/freckle-mcp`. This folder contains the complete Claude package.
The repository root and `freckle-mcp/` are not Claude submission folders.

[Website](https://freckle.io) · [Privacy policy](https://freckle.io/privacy-policy) ·
[Terms](https://freckle.io/terms-of-service) ·
[Support](https://form.typeform.com/to/ckOxY4xr?typeform-source=www.freckle.io)
