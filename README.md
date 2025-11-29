> Server-less data pipeline designed to capture, process, and analyse high-frequency YouTube video metadata in real-time. This system needs to achieve subsystem latency from video publication to database storage while maintaining production-grade reliability, idempotency, and cost effective.

### Goal
- To build a real-time YouTube monitoring using cloud technologies and agentic AI. 
- Basically:
	1. Watch certain YouTube channels. 
	2. Detect instantly when then publish something 
	3. Store all video metadata into a cloud DB
	4. Expose an API that returns the newest videos from the DB. 
	5. Build an agentic AI chatbot that can query this database using agents/tools. 
- Real-time data engineering and LLM pipeline

### Summary
- Build a real-time YouTube monitoring system.
- Use WebSub (webhooks) -> NO Polling
- Store data in MongoDB
- Make the ingestion Idempotent.
- Query new videos using FastAPI.
- Deploy endpoints using serverless cloud functions.
- create an Agentic AI chatbot that uses tools to query the DB.

### Tools to use
1. Python (FastAPI)
2. MongoDB 
3. Streamlit 
4. API Gateway + AWS Lambda 
5. Google ADK 
6. YouTube Web-Sub API's

### Project structure
```text
/webhook/          # serverless webhook function (fastapi or minimal)
/worker/           # worker service that enriches & upserts
/fastapi/          # FastAPI query API + auth
/agents/           # google-adk agent code (python)
/ui/               # streamlit UI code
/infra/            # Terraform configs
/scripts/          # bulk-import, local dev scripts
/docs/             # diagrams, runbook, credentials instructions
/config/           # all the configuration files
```
