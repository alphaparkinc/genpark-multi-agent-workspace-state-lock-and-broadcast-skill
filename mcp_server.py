"""MCP server for Multi-Agent State Lock Manager."""
import sys
import json
from client import MultiAgentStateLockManager

_lock_mgr = MultiAgentStateLockManager()

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "acquire_resource_lock",
                    "description": "Acquires exclusive distributed lock on a shared workspace resource",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "resource_id": {"type": "string"},
                            "agent_id": {"type": "string"},
                            "ttl_sec": {"type": "integer"}
                        },
                        "required": ["resource_id", "agent_id"]
                    }
                },
                {
                    "name": "release_resource_lock",
                    "description": "Releases exclusive distributed lock on a resource",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "resource_id": {"type": "string"},
                            "agent_id": {"type": "string"}
                        },
                        "required": ["resource_id", "agent_id"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "acquire_resource_lock":
            res = _lock_mgr.acquire_lock(args.get("resource_id", ""), args.get("agent_id", ""), args.get("ttl_sec", 30))
            return {"content": [{"type": "text", "text": json.dumps({"acquired": res})}]}
        elif tool_name == "release_resource_lock":
            res = _lock_mgr.release_lock(args.get("resource_id", ""), args.get("agent_id", ""))
            return {"content": [{"type": "text", "text": json.dumps({"released": res})}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
