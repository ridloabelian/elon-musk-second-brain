#!/usr/bin/env python3
import os, sys, glob, re

def search(query):
    print(f"🧠 Querying Elon Brain for: '{query}'...\n")
    files = glob.glob('**/*.md', recursive=True)
    found = False
    for f in files:
        if f in ['README.md', 'LICENSE']: continue
        with open(f, 'r') as file:
            content = file.read()
            if re.search(query, content, re.IGNORECASE):
                found = True
                print(f"🎯 MATCH FOUND IN: {f}")
                print("-" * 40)
                # Print matching context (simplified)
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if re.search(query, line, re.IGNORECASE):
                        start = max(0, i - 1)
                        end = min(len(lines), i + 2)
                        print("\n".join(lines[start:end]))
                        print("...")
                print("-" * 40 + "\n")
    
    if not found:
        print("❌ No matches found. You need to think harder.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 brain.py <query>")
        sys.exit(1)
    search(sys.argv[1])
