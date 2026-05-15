# System State Pipeline - Native Implementation

## Architecture
This implementation rejects PR #52 to avoid additive dependency bloat. State synchronization and race condition mitigation (Issue #26) are handled via native Lua scripts executed at the data layer.

## Requirements
- memanto-sdk
- langchain (Python)

## Execution
1. Run Python ingestion to initialize state and execute LangChain tool:
   `python3 full_pipeline_demo.py`
2. Run JS verification to prove cross-process persistence:
   `node full_pipeline_demo.js`

## Design Constraints
- Zero-dependency locking logic.
- Atomic transitions via Lua.
- Shared AGENT_ID namespace for ingestion and recall.
