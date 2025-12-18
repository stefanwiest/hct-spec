#!/usr/bin/env python3
"""
HCT Spec Code Generator

Generates code for all target languages from spec.yaml.
This is THE single source of truth generator.

Outputs:
- schema.json: JSON Schema for validation
- generated/python/: Python enums and types
- generated/typescript/: TypeScript enums and interfaces
- generated/go/: Go constants and types
- generated/rust/: Rust enums and structs
"""

import json
import yaml
from pathlib import Path
from datetime import datetime


def load_spec() -> dict:
    """Load spec.yaml"""
    spec_path = Path(__file__).parent.parent / "spec.yaml"
    with open(spec_path) as f:
        return yaml.safe_load(f)


def generate_json_schema(spec: dict) -> dict:
    """Generate JSON Schema from spec"""
    signals = list(spec.get("signals", {}).keys())
    tempo_values = list(spec.get("performance", {}).get("tempo", {}).get("values", {}).keys())
    dynamics_values = list(spec.get("performance", {}).get("dynamics", {}).get("values", {}).keys())
    
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/stefanwiest/hct-spec/schema.json",
        "title": "HCT Signal Schema",
        "description": f"JSON Schema for HCT coordination signals. Generated {datetime.utcnow().isoformat()}Z",
        "type": "object",
        "properties": {
            "hct_signal": {
                "type": "object",
                "required": ["type", "source"],
                "properties": {
                    "type": {"type": "string", "enum": signals},
                    "source": {"type": "string"},
                    "targets": {"type": "array", "items": {"type": "string"}},
                    "performance": {
                        "type": "object",
                        "properties": {
                            "tempo": {"type": "string", "enum": tempo_values},
                            "dynamics": {"type": "string", "enum": dynamics_values},
                            "urgency": {"type": "integer", "minimum": 1, "maximum": 10},
                            "timeout_ms": {"type": "integer", "minimum": 0}
                        }
                    },
                    "conditions": {
                        "type": "object",
                        "properties": {
                            "hold_type": {"type": "string", "enum": ["human", "governance", "resource", "quality"]},
                            "quality_threshold": {"type": "number", "minimum": 0, "maximum": 1},
                            "repeat_until": {"type": "string"}
                        }
                    },
                    "context": {
                        "type": "object",
                        "properties": {
                            "movement": {"type": "string"},
                            "objectives": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "timestamp": {"type": "string", "format": "date-time"}
                }
            }
        }
    }
    return schema


def generate_python(spec: dict) -> str:
    """Generate Python enums"""
    signals = spec.get("signals", {})
    tempo = spec.get("performance", {}).get("tempo", {}).get("values", {})
    dynamics = spec.get("performance", {}).get("dynamics", {}).get("values", {})
    
    lines = [
        '"""',
        'HCT Signal Types - Auto-generated from hct-spec/spec.yaml',
        f'Generated: {datetime.utcnow().isoformat()}Z',
        '',
        'DO NOT EDIT MANUALLY - Edit spec.yaml and regenerate.',
        '"""',
        '',
        'from enum import Enum',
        '',
        '',
        'class SignalType(str, Enum):',
        '    """HCT coordination signal types."""',
    ]
    
    for name, info in signals.items():
        desc = info.get("description", "")
        lines.append(f'    {name.upper()} = "{name}"  # {desc}')
    
    lines.extend(['', '', 'class Tempo(str, Enum):', '    """Musical tempo indications."""'])
    for name, info in tempo.items():
        desc = info.get("description", "")
        lines.append(f'    {name.upper()} = "{name}"  # {desc}')
    
    lines.extend(['', '', 'class DynamicsLevel(str, Enum):', '    """Resource intensity levels."""'])
    for name, info in dynamics.items():
        full_name = info.get("name", name)
        lines.append(f'    {name.upper()} = "{name}"  # {full_name}')
    
    lines.append('')
    return '\n'.join(lines)


def generate_typescript(spec: dict) -> str:
    """Generate TypeScript enums"""
    signals = spec.get("signals", {})
    tempo = spec.get("performance", {}).get("tempo", {}).get("values", {})
    dynamics = spec.get("performance", {}).get("dynamics", {}).get("values", {})
    
    lines = [
        '/**',
        ' * HCT Signal Types - Auto-generated from hct-spec/spec.yaml',
        f' * Generated: {datetime.utcnow().isoformat()}Z',
        ' *',
        ' * DO NOT EDIT MANUALLY - Edit spec.yaml and regenerate.',
        ' */',
        '',
        'export enum SignalType {',
    ]
    
    for name, info in signals.items():
        desc = info.get("description", "")
        lines.append(f"    /** {desc} */")
        lines.append(f"    {name.upper()} = '{name}',")
    lines.append('}')
    
    lines.extend(['', 'export enum Tempo {'])
    for name, info in tempo.items():
        desc = info.get("description", "")
        lines.append(f"    /** {desc} */")
        lines.append(f"    {name.upper()} = '{name}',")
    lines.append('}')
    
    lines.extend(['', 'export enum DynamicsLevel {'])
    for name, info in dynamics.items():
        full_name = info.get("name", name)
        lines.append(f"    /** {full_name} */")
        lines.append(f"    {name.upper()} = '{name}',")
    lines.append('}')
    
    lines.append('')
    return '\n'.join(lines)


def generate_go(spec: dict) -> str:
    """Generate Go constants"""
    signals = spec.get("signals", {})
    tempo = spec.get("performance", {}).get("tempo", {}).get("values", {})
    dynamics = spec.get("performance", {}).get("dynamics", {}).get("values", {})
    
    lines = [
        '// HCT Signal Types - Auto-generated from hct-spec/spec.yaml',
        f'// Generated: {datetime.utcnow().isoformat()}Z',
        '//',
        '// DO NOT EDIT MANUALLY - Edit spec.yaml and regenerate.',
        '',
        'package hctmcpsignals',
        '',
        '// SignalType defines the HCT coordination signals.',
        'type SignalType string',
        '',
        'const (',
    ]
    
    for i, (name, info) in enumerate(signals.items()):
        desc = info.get("description", "")
        cap_name = name.capitalize()
        if i == 0:
            lines.append(f'\t{cap_name} SignalType = "{name}" // {desc}')
        else:
            lines.append(f'\t{cap_name} SignalType = "{name}" // {desc}')
    lines.append(')')
    
    lines.extend(['', '// Tempo defines urgency timing.', 'type Tempo string', '', 'const ('])
    for name, info in tempo.items():
        desc = info.get("description", "")
        cap_name = name.capitalize()
        lines.append(f'\t{cap_name} Tempo = "{name}" // {desc}')
    lines.append(')')
    
    lines.extend(['', '// DynamicsLevel defines resource intensity.', 'type DynamicsLevel string', '', 'const ('])
    for name, info in dynamics.items():
        full_name = info.get("name", name)
        cap_name = name.upper()
        lines.append(f'\tDynamics{cap_name} DynamicsLevel = "{name}" // {full_name}')
    lines.append(')')
    
    lines.append('')
    return '\n'.join(lines)


def generate_rust(spec: dict) -> str:
    """Generate Rust enums"""
    signals = spec.get("signals", {})
    tempo = spec.get("performance", {}).get("tempo", {}).get("values", {})
    dynamics = spec.get("performance", {}).get("dynamics", {}).get("values", {})
    
    lines = [
        '//! HCT Signal Types - Auto-generated from hct-spec/spec.yaml',
        f'//! Generated: {datetime.utcnow().isoformat()}Z',
        '//!',
        '//! DO NOT EDIT MANUALLY - Edit spec.yaml and regenerate.',
        '',
        'use serde::{Deserialize, Serialize};',
        '',
        '/// The HCT coordination signal types.',
        '#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]',
        '#[serde(rename_all = "lowercase")]',
        'pub enum SignalType {',
    ]
    
    for name, info in signals.items():
        desc = info.get("description", "")
        cap_name = name.capitalize()
        lines.append(f'    /// {desc}')
        lines.append(f'    {cap_name},')
    lines.append('}')
    
    lines.extend([
        '',
        '/// Musical tempo indications.',
        '#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, Default)]',
        '#[serde(rename_all = "lowercase")]',
        'pub enum Tempo {'
    ])
    for i, (name, info) in enumerate(tempo.items()):
        desc = info.get("description", "")
        cap_name = name.capitalize()
        lines.append(f'    /// {desc}')
        if name == "moderato":
            lines.append('    #[default]')
        lines.append(f'    {cap_name},')
    lines.append('}')
    
    lines.extend([
        '',
        '/// Resource intensity levels.',
        '#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, Default)]',
        '#[serde(rename_all = "lowercase")]',
        'pub enum DynamicsLevel {'
    ])
    for name, info in dynamics.items():
        full_name = info.get("name", name)
        cap_name = name.upper()
        lines.append(f'    /// {full_name}')
        if name == "mf":
            lines.append('    #[default]')
        lines.append(f'    {cap_name},')
    lines.append('}')
    
    lines.append('')

    return '\n'.join(lines)

def generate_protobuf(spec: dict) -> str:
    """Generate Protobuf definition"""
    signals = spec.get("signals", {})
    tempo = spec.get("performance", {}).get("tempo", {}).get("values", {})
    dynamics = spec.get("performance", {}).get("dynamics", {}).get("values", {})
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    lines = [
        'syntax = "proto3";',
        '',
        'package hct.v1;',
        '',
        'option go_package = "github.com/stefanwiest/hct-a2a/spec/v1;hct";',
        '',
        '// HCT Signal Types - Auto-generated from hct-spec/spec.yaml',
        f'// Generated: {timestamp}',
        '//',
        '// DO NOT EDIT MANUALLY - Edit spec.yaml and regenerate.',
        '',
        '// HCT A2A Extension Signal',
        'message HctSignal {',
        '  SignalType signal = 1;',
        '  string from = 2;',
        '  PerformanceDetails performance = 3;',
        '  ConditionDetails conditions = 4;',
        '  ContextDetails context = 5;',
        '}',
        '',
        'enum SignalType {',
        '  SIGNAL_TYPE_UNSPECIFIED = 0;',
    ]
    
    for i, (name, info) in enumerate(signals.items()):
        desc = info.get("description", "")
        lines.append(f'  {name.upper()} = {i + 1}; // {desc}')
    lines.append('}')
    
    lines.extend([
        '',
        'message PerformanceDetails {',
        '  Tempo tempo = 1;',
        '  Dynamics dynamics = 2;',
        '  int32 urgency = 3; // 1-10',
        '  int32 timeout_ms = 4;',
        '}',
        '',
        'enum Tempo {',
        '  TEMPO_UNSPECIFIED = 0;'
    ])
    
    for i, (name, info) in enumerate(tempo.items()):
        desc = info.get("description", "")
        lines.append(f'  {name.upper()} = {i + 1}; // {desc}')
    lines.append('}')
    
    lines.extend([
        '',
        'enum Dynamics {',
        '  DYNAMICS_UNSPECIFIED = 0;'
    ])
    
    for i, (name, info) in enumerate(dynamics.items()):
        full_name = info.get("name", name)
        lines.append(f'  {name.upper()} = {i + 1}; // {full_name}')
    lines.append('}')
    
    lines.extend([
        '',
        'message ConditionDetails {',
        '  HoldType hold_type = 1;',
        '  float quality_threshold = 2;',
        '  string repeat_until = 3;',
        '}',
        '',
        'enum HoldType {',
        '  HOLD_TYPE_UNSPECIFIED = 0;',
        '  HUMAN = 1;',
        '  GOVERNANCE = 2;',
        '  RESOURCE = 3;',
        '  QUALITY = 4;',
        '}',
        '',
        'message ContextDetails {',
        '  string movement = 1;',
        '  repeated string objectives = 2;',
        '}'
    ])
    
    return '\n'.join(lines)



def main():
    spec = load_spec()
    output_dir = Path(__file__).parent.parent
    
    # Generate JSON Schema
    schema = generate_json_schema(spec)
    schema_path = output_dir / "schema.json"
    with open(schema_path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"✓ Generated {schema_path}")
    
    # Create generated directory
    gen_dir = output_dir / "generated"
    gen_dir.mkdir(exist_ok=True)
    
    # Python
    py_dir = gen_dir / "python"
    py_dir.mkdir(exist_ok=True)
    with open(py_dir / "types.py", "w") as f:
        f.write(generate_python(spec))
    print(f"✓ Generated {py_dir}/types.py")
    
    # TypeScript
    ts_dir = gen_dir / "typescript"
    ts_dir.mkdir(exist_ok=True)
    with open(ts_dir / "types.ts", "w") as f:
        f.write(generate_typescript(spec))
    print(f"✓ Generated {ts_dir}/types.ts")
    
    # Go
    go_dir = gen_dir / "go"
    go_dir.mkdir(exist_ok=True)
    with open(go_dir / "types.go", "w") as f:
        f.write(generate_go(spec))
    print(f"✓ Generated {go_dir}/types.go")
    
    # Rust
    rust_dir = gen_dir / "rust"
    rust_dir.mkdir(exist_ok=True)
    with open(rust_dir / "types.rs", "w") as f:
        f.write(generate_rust(spec))
    print(f"✓ Generated {rust_dir}/types.rs")
    
    # Protobuf
    proto_dir = gen_dir / "protobuf"
    proto_dir.mkdir(exist_ok=True)
    with open(proto_dir / "hct.proto", "w") as f:
        f.write(generate_protobuf(spec))
    print(f"✓ Generated {proto_dir}/hct.proto")
    
    # Summary
    signals = list(spec.get("signals", {}).keys())
    print(f"\n📋 Spec: {len(signals)} signals")
    print(f"   {', '.join(signals)}")


if __name__ == "__main__":
    main()
