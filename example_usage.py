"""Example usage for Multi-Agent State Lock Manager."""
from client import MultiAgentStateLockManager

if __name__ == "__main__":
    manager = MultiAgentStateLockManager()
    ok = manager.acquire_lock("build_artifact_12", "compiler_agent", ttl_sec=60)
    print("Lock Acquired:", ok)
    manager.release_lock("build_artifact_12", "compiler_agent")
    print("Lock Released.")
