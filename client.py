"""Multi-Agent Workspace State Lock & Broadcast.
100% Python Standard Library.
"""

import time

class MultiAgentStateLockManager:
    """Manages distributed locks on resources and broadcasts change events to peer agents."""
    
    def __init__(self):
        self.locks = {}
        self.event_bus = []
        
    def acquire_lock(self, resource_id: str, agent_id: str, ttl_sec: int = 30) -> bool:
        now = time.time()
        current_lock = self.locks.get(resource_id)
        if current_lock and current_lock["expires_at"] > now and current_lock["agent_id"] != agent_id:
            return False
            
        self.locks[resource_id] = {
            "agent_id": agent_id,
            "acquired_at": now,
            "expires_at": now + ttl_sec
        }
        self.event_bus.append({
            "type": "LOCK_ACQUIRED",
            "resource": resource_id,
            "agent": agent_id,
            "timestamp": now
        })
        return True
        
    def release_lock(self, resource_id: str, agent_id: str) -> bool:
        current_lock = self.locks.get(resource_id)
        if not current_lock or current_lock["agent_id"] != agent_id:
            return False
        del self.locks[resource_id]
        self.event_bus.append({
            "type": "LOCK_RELEASED",
            "resource": resource_id,
            "agent": agent_id,
            "timestamp": time.time()
        })
        return True
