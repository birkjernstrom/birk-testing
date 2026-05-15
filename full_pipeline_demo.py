import os
from langchain.tools import Tool
from memanto.cli.client.sdk_client import SdkClient

def execute_atomic_state_transition(agent_id, key, expected_val, new_val):
    """
    Bypasses external locking libraries by executing a Lua script on the 
    data layer to ensure atomicity and prevent race conditions in #26.
    """
    client = SdkClient()
    lua_script = """
    local current = redis.call('GET', KEYS[1])
    if current == ARGV[1] then
        redis.call('SET', KEYS[1], ARGV[2])
        return 1
    end
    return 0
    """
    # Atomic operation performed at the server level to eliminate client-side sync bloat
    return client.eval(lua_script, keys=[f"{agent_id}:{key}"], args=[expected_val, new_val])

def run_ingestion_cycle():
    sync_agent_id = "sys_eng_prod_01"
    persistence_client = SdkClient()
    
    state_payload = "initialized"
    persistence_client.set(f"{sync_agent_id}:status", state_payload)
    
    # Binding Memanto logic as a LangChain Tool to avoid plain text instruction reliance
    state_tool = Tool(
        name="AtomicStateUpdate",
        func=lambda input_str: execute_atomic_state_transition(
            sync_agent_id, "status", "initialized", input_str
        ),
        description="Updates the system state atomically"
    )
    
    result = state_tool.run("active")
    print(f"Atomic transition result: {result}")
    return sync_agent_id

if __name__ == "__main__":
    agent_id = run_ingestion_cycle()
    print(f"Ingestion complete for AGENT_ID: {agent_id}")
