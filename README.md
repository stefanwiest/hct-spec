# HCT Specification

**THE single source of truth for HCT protocol elements.**

## Files

- **`spec.yaml`** - Signal and performance definitions

## Signals

| Signal | Scope | Description |
|--------|-------|-------------|
| `cue` | MCP + A2A | Trigger activation |
| `fermata` | MCP + A2A | Hold for approval |
| `attacca` | MCP + A2A | Immediate transition |
| `vamp` | MCP + A2A | Repeat until condition |
| `caesura` | MCP + A2A | Full stop |
| `tacet` | A2A only | Agent inactive |
| `downbeat` | A2A only | Global sync point |

## Related

- [hct-mcp-signals](https://github.com/stefanwiest/hct-mcp-signals)
- [hct-a2a](https://github.com/stefanwiest/hct-a2a)
