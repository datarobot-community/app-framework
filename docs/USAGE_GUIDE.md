# How to use DataRobot skills

## Overview

DataRobot skills work like Hugging Face skills: they guide your coding agent to use the **DataRobot Python SDK** directly. No server component is required.

## How it works

```text
User → Coding Agent → Skill Instructions → Python Code (using SDK) → DataRobot API
```

1. **User installs a skill** (for example, `datarobot-predictions`).
2. **User asks the agent** to do something (for example, "Generate a prediction dataset template").
3. **The agent reads the skill** in `datarobot-predictions/SKILL.md`.
4. **The agent writes Python code** with the DataRobot SDK based on the skill instructions.
5. **The agent executes the code** and returns the results.

## Prerequisites

- **DataRobot account** with API access
- **DataRobot API token** and endpoint
- **Python environment** where your coding agent can install packages
- **Coding agent** (Claude Code, Cursor, Codex, etc.)

The agent will automatically install the `datarobot` Python package when needed.

## Installation

### Claude Code

```bash
/plugin marketplace add datarobot-oss/datarobot-agent-skills
/plugin install datarobot-predictions@datarobot-skills
```

### Codex

Codex automatically reads `AGENTS.md`, so no installation is needed.

### Gemini CLI

```bash
gemini extensions install https://github.com/datarobot-oss/datarobot-agent-skills.git --consent
```

## Usage examples

### Example 1: Generate prediction dataset template

**User**: "Generate a prediction dataset template for deployment abc123 with 10 rows"

**Agent workflow**:
1. Reads `datarobot-predictions/SKILL.md`
2. Sees workflow example and code patterns
3. Writes Python code:
   ```python
   import datarobot as dr
   import pandas as pd
   
   client = dr.Client(token=..., endpoint=...)
   deployment = dr.Deployment.get("abc123")
   model = dr.Model.get(deployment.model['id'])
   features = model.get_features()
   # ... generates template DataFrame ...
   ```
4. Executes code and returns CSV template

### Example 2: Train a model

**User**: "Create a new project with sales_data.csv, set 'revenue' as target, and start Quick AutoML"

**Agent workflow**:
1. Reads `skills/datarobot-model-training/SKILL.md`
2. Follows the workflow example
3. Writes Python code:
   ```python
   import datarobot as dr
   
   dataset = dr.Dataset.create_from_file("sales_data.csv", "Sales Data")
   project = dr.Project.create_from_dataset(dataset.id, "Sales Prediction")
   project.set_target("revenue", mode=dr.AUTOPILOT_MODE.QUICK)
   project.start(autopilot_on=True)
   ```
4. Executes code and monitors training

## What skills provide

Each skill includes:

1. **Quick start** - The most common use case with a three-step workflow
2. **When to use** - When the skill is appropriate
3. **Key capabilities** - What you can do with the skill
4. **Workflow examples** - Step-by-step agent workflows
5. **Using DataRobot SDK** - SDK operations and methods
6. **Common patterns** - Complete code examples
7. **Best practices** - Tips and recommendations
8. **SDK setup** - How to install and initialize the SDK

## SDK usage summary

### Primary approach: Direct SDK usage

**How it works**:
- Agent installs `datarobot` package
- Agent writes Python code using SDK
- Agent executes code directly
- No server needed

**Example**:
```python
import datarobot as dr
import os
import pandas as pd

client = dr.Client(
    token=os.getenv("DATAROBOT_API_TOKEN"),
    endpoint=os.getenv("DATAROBOT_ENDPOINT", "https://app.datarobot.com")
)

deployment = dr.Deployment.get("abc123")
predictions_df = deployment.predict_batch(pd.DataFrame([data]))
print(predictions_df)
```

### Optional: MCP server

If you have a DataRobot MCP server running, agents can also use MCP tools as an alternative. This provides:

- Standardized tool interface
- Better security (credentials on server)
- Dynamic tool registration

However, an **MCP server is not required**. Skills work with direct SDK usage.

## Environment setup

The agent needs these environment variables:

```bash
export DATAROBOT_API_TOKEN="your-api-token"
export DATAROBOT_ENDPOINT="https://app.datarobot.com"
```

Or the agent can prompt the user for these values.

## Complete workflow example

**User request**: "I want to predict sales for next week for store_A with temperatures of 75°F each day and no promotions."

**Agent (using datarobot-predictions skill)**:

1. **Reads skill** → Understands workflow
2. **Gets deployment features**:
   ```python
   deployment = dr.Deployment.get("sales_deployment")
   model = dr.Model.get(deployment.model['id'])
   features = model.get_features()
   ```
3. **Generates template**:
   ```python
   # Creates DataFrame with required columns
   template_df = pd.DataFrame(...)
   ```
4. **Fills template** with user's values (store_A, next 7 days, temp=75, promotion=0)
5. **Validates data** (checks types, required columns)
6. **Makes predictions**:
   ```python
   predictions_df = deployment.predict_batch(filled_data)
   ```
7. **Returns results** to user

## Best practices

1. **Install skills** for workflows you use frequently
2. **Provide API credentials** to your agent (securely)
3. **Use specific requests** - "Generate template for deployment abc123" vs "Make predictions"
4. **Review generated code** - Agent writes code based on skills, review before execution
5. **Use multiple skills** - Combine skills for complex workflows

## Troubleshooting

### SDK Not Found
- Agent should install: `pip install datarobot`
- Check Python environment

### Authentication Errors
- Verify `DATAROBOT_API_TOKEN` is set
- Check `DATAROBOT_ENDPOINT` is correct
- Ensure token has necessary permissions

### Import Errors

- Ensure `datarobot` package is installed
- Check Python version (3.7+)

## Additional resources

- [DataRobot Python SDK Documentation](https://datarobot-public-api-client.readthedocs-hosted.com/)
- [DataRobot API Documentation](https://docs.datarobot.com/en/docs/api/reference/index.html)
- [Skill documentation](../README.md) - A list of all available skills

