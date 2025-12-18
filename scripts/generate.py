#!/usr/bin/env python3
"""
Generate JSON Schema from spec.yaml

This is the code generation script for HCT specification.
"""

import json
import yaml
from pathlib import Path


def load_spec() -> dict:
    """Load spec.yaml"""
    spec_path = Path(__file__).parent.parent / "spec.yaml"
    with open(spec_path) as f:
        return yaml.safe_load(f)


def generate_json_schema(spec: dict) -> dict:
    """Generate JSON Schema from spec"""
    
    # Extract signal names
    signals = list(spec.get("signals", {}).keys())
    
    # Extract tempo values
    tempo_values = list(spec.get("performance", {}).get("tempo", {}).get("values", {}).keys())
    
    # Extract dynamics values
    dynamics_values = list(spec.get("performance", {}).get("dynamics", {}).get("values", {}).keys())
    
    # Build JSON Schema
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://github.com/stefanwiest/hct-spec/schema.json",
        "title": "HCT Signal Schema",
        "description": "JSON Schema for HCT coordination signals",
        "type": "object",
        "properties": {
            "hct_signal": {
                "type": "object",
                "required": ["type", "source"],
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": signals,
                        "description": "Signal type"
                    },
                    "source": {
                        "type": "string",
                        "description": "Source agent ID"
                    },
                    "targets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Target agent IDs"
                    },
                    "performance": {
                        "type": "object",
                        "properties": {
                            "tempo": {
                                "type": "string",
                                "enum": tempo_values,
                                "default": spec.get("performance", {}).get("tempo", {}).get("default", "moderato")
                            },
                            "dynamics": {
                                "type": "string", 
                                "enum": dynamics_values,
                                "default": spec.get("performance", {}).get("dynamics", {}).get("default", "mf")
                            },
                            "urgency": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "default": 5
                            },
                            "timeout_ms": {
                                "type": "integer",
                                "minimum": 0
                            }
                        }
                    },
                    "conditions": {
                        "type": "object",
                        "properties": {
                            "hold_type": {
                                "type": "string",
                                "enum": ["human", "governance", "resource", "quality"]
                            },
                            "quality_threshold": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1
                            },
                            "repeat_until": {
                                "type": "string"
                            }
                        }
                    },
                    "context": {
                        "type": "object",
                        "properties": {
                            "movement": {"type": "string"},
                            "objectives": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    },
                    "timestamp": {
                        "type": "string",
                        "format": "date-time"
                    }
                }
            }
        }
    }
    
    return schema


def main():
    spec = load_spec()
    schema = generate_json_schema(spec)
    
    output_path = Path(__file__).parent.parent / "schema.json"
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)
    
    print(f"Generated {output_path}")
    print(f"  Signals: {list(spec.get('signals', {}).keys())}")
    print(f"  Tempo: {list(spec.get('performance', {}).get('tempo', {}).get('values', {}).keys())}")
    print(f"  Dynamics: {list(spec.get('performance', {}).get('dynamics', {}).get('values', {}).keys())}")


if __name__ == "__main__":
    main()
