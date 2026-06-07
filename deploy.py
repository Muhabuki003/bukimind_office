#!/usr/bin/env python3
"""Trigger a Cloudflare Pages deployment for bukimind-office."""
import subprocess, json, os

with open('/tmp/cf_token.txt') as f:
    cf_token = f.read().strip()

token = cf_token
account_id = "a9c77b1cff6d48f28930ed068bbba95e"
project = "bukimind-office"

# Create a deployment
result = subprocess.run(
    ["curl", "-s", "-X", "POST",
     "-H", f"Authorization: Bearer {token}",
     "-H", "Content-Type: application/json",
     "-d", '{"branch":"main"}',
     f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project}/deployments"],
    capture_output=True, text=True, timeout=30
)

data = json.loads(result.stdout)
if data.get("success"):
    depl = data["result"]
    print(f"✅ Deploy triggered!")
    print(f"   URL: {depl.get('url', 'N/A')}")
    print(f"   Status: {depl.get('status', 'N/A')}")
    print(f"   ID: {depl.get('id', 'N/A')}")
else:
    print(f"❌ Failed: {data.get('errors', [{}])[0].get('message', 'unknown')}")
