# HCT Specification

**THE single source of truth for HCT protocol elements.**

[![CI](https://github.com/stefanwiest/hct-spec/actions/workflows/generate.yml/badge.svg)](https://github.com/stefanwiest/hct-spec/actions)

---

## Overview

This repository defines the canonical specification for Harmonic Coordination Theory signals and performance parameters. All downstream packages are auto-generated from this spec.

## Files

| File | Purpose |
|------|---------|
| `spec.yaml` | Signal and performance definitions |
| `schema.json` | JSON Schema (auto-generated) |
| `generated/` | Language-specific types (auto-generated) |

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

## Performance

| Parameter | Values | Description |
|-----------|--------|-------------|
| `tempo` | largo, andante, moderato, allegro, presto | Urgency/timing |
| `dynamics` | pp, p, mf, f, ff | Resource intensity |

## Generated Outputs

When `spec.yaml` changes, CI automatically generates:

- **Python**: `generated/python/types.py` → synced to `hct-mcp-signals/python/hct_mcp_signals/spec.py`
- **TypeScript**: `generated/typescript/types.ts` → synced to `hct-mcp-signals/npm/src/spec.ts`
- **Go**: `generated/go/types.go` → synced to `hct-mcp-signals/go/spec.go`
- **Rust**: `generated/rust/types.rs` → synced to `hct-mcp-signals/rust/src/spec.rs`
- **JSON Schema**: `schema.json` → synced to both packages

## Downstream Packages

- [hct-mcp-signals](https://github.com/stefanwiest/hct-mcp-signals) - MCP extension (Python, npm, Rust, Go)
- [hct-a2a](https://github.com/stefanwiest/hct-a2a) - A2A extension

## License

Apache 2.0
