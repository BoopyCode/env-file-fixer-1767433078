#!/usr/bin/env python3
"""
.env Wrangler - Because your environment variables need a stern talking-to.
Tames wild .env files by showing differences between environments.
"""

import sys
import os
from pathlib import Path

def parse_env_file(filepath):
    """Reads .env files, ignoring comments and empty lines.
    Returns dict of key-value pairs.
    """
    env_vars = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # Skip comments and empty lines
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
    return env_vars

def compare_envs(env1, env2, name1="local", name2="staging"):
    """Compares two environment dicts and prints differences.
    Because 'it works on my machine' is the developer's mating call.
    """
    all_keys = set(env1.keys()) | set(env2.keys())
    differences = []
    
    for key in sorted(all_keys):
        val1 = env1.get(key, "<MISSING>")
        val2 = env2.get(key, "<MISSING>")
        
        if val1 != val2:
            differences.append((key, val1, val2))
    
    if not differences:
        print(f"🎉 No differences! {name1} and {name2} are identical twins.")
        return
    
    print(f"🔍 Found {len(differences)} difference(s) between {name1} and {name2}:")
    print("-" * 60)
    for key, val1, val2 in differences:
        print(f"{key}:")
        print(f"  {name1}: {val1}")
        print(f"  {name2}: {val2}")
        print()

def main():
    """Main function - because every script needs a leader."""
    if len(sys.argv) < 3:
        print("Usage: python env_wrangler.py <env1> <env2> [name1] [name2]")
        print("Example: python env_wrangler.py .env.local .env.staging local staging")
        sys.exit(1)
    
    file1, file2 = sys.argv[1], sys.argv[2]
    name1 = sys.argv[3] if len(sys.argv) > 3 else "env1"
    name2 = sys.argv[4] if len(sys.argv) > 4 else "env2"
    
    env1 = parse_env_file(file1)
    env2 = parse_env_file(file2)
    
    if not env1 and not env2:
        print("🤷 Both files are empty or missing. Nothing to wrangle!")
        return
    
    compare_envs(env1, env2, name1, name2)

if __name__ == "__main__":
    main()
