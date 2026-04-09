# Adding a vector database to your agent app

You've got an agent application running and it's doing its thing — but you want to ground it in your own documents. Maybe you've got a knowledge base, some internal docs, or a collection of PDFs that your agent should actually know about instead of making things up.

This guide walks through adding a Vector Database (VDB) to your agent app. A folder of documents becomes searchable, semantic knowledge your agent can use for retrieval.

## Prerequisites

- An App Framework recipe with the [Agentic Starter Application](https://github.com/datarobot/recipe-datarobot-agent-application) or similar setup
- The LLM component applied

## The setup

First, tell your infrastructure to use the LLM configuration that supports vector databases. In your `.env`:

```bash
INFRA_ENABLE_LLM="blueprint_with_llm_gateway.py"
```

This switches to an LLM Blueprint that supports VDB retrieval alongside the LLM Gateway.

## Your knowledge base

Create a `knowledgebase/` folder at the root of your project and add your documents — PDFs, text files, markdown, whatever you've got:

```
your-project/
├── knowledgebase/
│   ├── important-doc.pdf
│   ├── team-guidelines.md
│   └── product-specs.txt
├── infra/
└── ...
```

This folder is version-controlled alongside your code. When you update your documents, just redeploy.

## The VDB infrastructure

Create `infra/infra/vdb.py`:

```python
"""
Vector DB Infrastructure: Dataset, Vector Database, and Deployment.
"""
import os
import shutil
import tempfile
from pathlib import Path

import pulumi
import pulumi_datarobot
from datarobot_pulumi_utils.pulumi import export
from datarobot_pulumi_utils.pulumi.stack import PROJECT_NAME

from . import project_dir, use_case

__all__ = [
    "knowledgebase_dataset",
    "vector_database",
]

KNOWLEDGEBASE_FOLDER_NAME = "knowledgebase"


def create_knowledgebase_zip() -> str:
    """Create a zip file of the knowledgebase folder."""
    knowledgebase_dir = project_dir.parent / "knowledgebase"

    if not knowledgebase_dir.exists():
        raise FileNotFoundError(
            f"Knowledgebase directory not found: {knowledgebase_dir}"
        )

    temp_dir = tempfile.mkdtemp()
    zip_path = Path(temp_dir) / KNOWLEDGEBASE_FOLDER_NAME
    shutil.make_archive(str(zip_path), "zip", knowledgebase_dir)
    return f"{zip_path}.zip"


knowledgebase_zip_path = create_knowledgebase_zip()

knowledgebase_dataset = pulumi_datarobot.DatasetFromFile(
    resource_name=f"Agentic Starter App Knowledgebase [{PROJECT_NAME}]",
    file_path=knowledgebase_zip_path,
    use_case_ids=[use_case.id],
    opts=pulumi.ResourceOptions(depends_on=[use_case]),
)

# Chunking parameters are all configurable via environment variables.
chunking_method = os.environ.get("VDB_CHUNKING_METHOD", "recursive")
chunk_size = int(os.environ.get("VDB_CHUNK_SIZE", "512"))
chunk_overlap = int(os.environ.get("VDB_CHUNK_OVERLAP_PERCENTAGE", "10"))
embedding_model = os.environ.get("VDB_EMBEDDING_MODEL", "intfloat/e5-large-v2")

vector_database = pulumi_datarobot.VectorDatabase(
    resource_name=f"Agentic Starter Application VDB [{PROJECT_NAME}]",
    use_case_id=use_case.id,
    dataset_id=knowledgebase_dataset.id,
    chunking_parameters=pulumi_datarobot.VectorDatabaseChunkingParametersArgs(
        chunking_method=chunking_method,
        chunk_size=chunk_size,
        chunk_overlap_percentage=chunk_overlap,
        embedding_model=embedding_model,
    ),
    opts=pulumi.ResourceOptions(depends_on=[use_case, knowledgebase_dataset]),
)

export("AGENTIC_STARTER_DATASET_ID", knowledgebase_dataset.id)
export("AGENTIC_STARTER_VECTOR_DATABASE_ID", vector_database.id)
```

This code:

1. Zips up your `knowledgebase/` folder.
2. Creates a DataRobot dataset from that zip.
3. Builds a vector database with configurable chunking (512 token chunks, 10% overlap by default).
4. Uses `intfloat/e5-large-v2` as the embedding model.

All chunking parameters are tunable via environment variables in your `.env` — no code changes required.

## Wire it up

Open `infra/infra/llm.py` and add the import at the top:

```python
from .vdb import vector_database
```

Then find where you create your `llm_blueprint` and add the `vector_database_id` parameter:

```python
llm_blueprint = datarobot.LlmBlueprint(
    resource_name="LLM Blueprint " + llm_resource_name,
    playground_id=playground.id,
    llm_id=default_llm_id,
    vector_database_id=vector_database.id,  # add this
    llm_settings=datarobot.LlmBlueprintLlmSettingsArgs(
        max_completion_length=2048,
        temperature=0.1,
        top_p=None,
    ),
)
```

That's it. Your agent is now grounded in your documents.

## Deploy and test

```bash
task deploy
```

Once deployed, your agent pulls relevant context from the knowledgebase instead of hallucinating. Ask it questions about your docs.

## Why this approach works

- **Version-controlled**&mdash;your knowledge base lives in git alongside your code.
- **Tunable without code changes**&mdash;chunking parameters are env vars.
- **Automatically rebuilt**&mdash;updating your docs is just adding files and redeploying.
- **Infrastructure-as-code**&mdash;the whole stack is reproducible.

## This works everywhere

This same approach works for any App Template — Talk to My Docs, Talk to My Data, any of them. The pattern is identical: create `vdb.py`, wire it into `llm.py`, redeploy.

## Pro tips

**Chunk sizes:**

- Smaller chunks (256–512 tokens)&mdash;better for precise, targeted retrieval.
- Larger chunks (1024+ tokens)&mdash;better when more context per retrieval hit is important.

**Embedding models:**

The default `intfloat/e5-large-v2` is solid for general use, but domain-specific embedding models may work better for specialized content (legal, medical, technical). Set `VDB_EMBEDDING_MODEL` in your `.env` to experiment without touching code.

**Multiple knowledge bases:**

Fork this pattern and create multiple `vdb.py` files — one per knowledge base. You can implement smart routing between VDBs in your agent logic to serve different document sets for different query types.
