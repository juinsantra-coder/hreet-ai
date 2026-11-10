# HREET AI Orange Nexus — Build 02

A local-first Windows starter with a real chat connection to Ollama. This build is a working foundation, not yet a full desktop OS or unrestricted PC agent.

## Requirements
- Windows 10/11
- Python 3.10+
- Ollama for real AI answers

## Start
1. Install Ollama from https://ollama.com/download/windows
2. Open PowerShell and run `ollama pull llama3.2`.
3. Run `ollama run llama3.2` once, then leave Ollama running.
4. Double-click `START_HREET_AI.bat` in this folder.
5. Open http://127.0.0.1:8000 if the browser does not open automatically.

## Notes
- Chat requests go to the local Ollama service at `127.0.0.1:11434`.
- The UI checks backend/model availability and reports connection errors instead of returning fake demo answers.
- This build does not yet control Windows, access personal files, pair Android, or provide persistent memory. Those need separate permission-gated modules.

## Configuration
Set `OLLAMA_MODEL` to another model name before starting the server if desired. Default: `llama3.2`.
