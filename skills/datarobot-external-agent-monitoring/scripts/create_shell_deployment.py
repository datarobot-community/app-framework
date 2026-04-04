#!/usr/bin/env python3
"""
Create a shell deployment in DataRobot for receiving external agent OTel telemetry.

Usage:
    python create_shell_deployment.py --name "My Agent" --description "OTel sink"

Env vars:
    DATAROBOT_API_TOKEN  - DataRobot API token
    DATAROBOT_ENDPOINT   - DataRobot API endpoint (default: https://app.datarobot.com)
"""

import argparse
import json
import os
import sys

import datarobot as dr


def create_shell_deployment(name: str, description: str) -> dict:
    """Create a shell deployment in DataRobot for external agent monitoring.

    Creates an external registered model (target type: AgenticWorkflow) and
    deploys it to an external prediction environment. The deployment ID is
    used to route OTel telemetry to the correct DataRobot dashboard.

    Args:
        name: Display name for the deployment
        description: Description of what agent this monitors

    Returns:
        Dict with deployment_id, entity_id, and otel_endpoint
    """
    token = os.getenv("DATAROBOT_API_TOKEN")
    endpoint = os.getenv("DATAROBOT_ENDPOINT", "https://app.datarobot.com")

    if not token:
        print("Error: DATAROBOT_API_TOKEN env var is required", file=sys.stderr)
        sys.exit(1)

    client = dr.Client(token=token, endpoint=endpoint)

    # Discover target type — prefer AgenticWorkflow, fall back to TextGeneration
    target_type = None
    try:
        # Try AgenticWorkflow first (required for proper monitoring dashboards)
        target_type = "AgenticWorkflow"
        # Validate by attempting to use it — the SDK may use an enum or string
        # Check if the SDK has the enum value
        if hasattr(dr.enums, "TARGET_TYPE"):
            tt_enum = dr.enums.TARGET_TYPE
            if hasattr(tt_enum, "AGENTIC_WORKFLOW"):
                target_type = tt_enum.AGENTIC_WORKFLOW
            elif hasattr(tt_enum, "AGENTICWORKFLOW"):
                target_type = tt_enum.AGENTICWORKFLOW
    except Exception:
        pass

    if target_type is None:
        print(
            "Warning: Could not find AgenticWorkflow target type. "
            "Falling back to TextGeneration. Monitoring dashboards may not "
            "display correctly.",
            file=sys.stderr,
        )
        target_type = "TextGeneration"

    # Create external registered model
    try:
        model_package = dr.RegisteredModel.create(
            name=name,
            target_type=target_type,
            description=description,
            is_external=True,
        )
    except Exception as e:
        # If AgenticWorkflow fails, retry with TextGeneration
        if "AgenticWorkflow" in str(target_type):
            print(
                f"Warning: AgenticWorkflow target type failed ({e}). "
                "Retrying with TextGeneration.",
                file=sys.stderr,
            )
            target_type = "TextGeneration"
            model_package = dr.RegisteredModel.create(
                name=name,
                target_type=target_type,
                description=description,
                is_external=True,
            )
        else:
            raise

    # Get or create an external prediction environment
    prediction_envs = dr.PredictionEnvironment.list()
    external_env = None
    for env in prediction_envs:
        if getattr(env, "platform", None) == "external":
            external_env = env
            break

    if external_env is None:
        external_env = dr.PredictionEnvironment.create(
            name="External Agent Environment",
            platform="external",
            description="Environment for external agent OTel monitoring",
        )

    # Deploy
    deployment = dr.Deployment.create_from_registered_model(
        registered_model_version=model_package.latest_version,
        label=name,
        description=description,
        prediction_environment_id=external_env.id,
    )

    # Build the OTel endpoint from the API endpoint
    # API endpoint is like https://app.datarobot.com/api/v2
    # OTel endpoint is like https://app.datarobot.com/otel
    base_url = endpoint.rstrip("/")
    if base_url.endswith("/api/v2"):
        base_url = base_url[: -len("/api/v2")]
    otel_endpoint = f"{base_url}/otel"

    return {
        "deployment_id": deployment.id,
        "entity_id": f"deployment-{deployment.id}",
        "otel_endpoint": otel_endpoint,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a DataRobot shell deployment for external agent monitoring"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Display name for the deployment",
    )
    parser.add_argument(
        "--description",
        default="External agent OTel telemetry sink",
        help="Description of what agent this monitors",
    )
    args = parser.parse_args()

    try:
        result = create_shell_deployment(args.name, args.description)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
