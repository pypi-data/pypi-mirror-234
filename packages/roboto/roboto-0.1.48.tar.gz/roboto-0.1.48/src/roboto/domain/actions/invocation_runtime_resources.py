import enum

ROBOTO_ENV_VAR_PREFIX = "ROBOTO_"


class InvocationEnvVar(str, enum.Enum):
    """Environment variables that are set by the Roboto Platform when invoking an action."""

    ActionParametersFile = f"{ROBOTO_ENV_VAR_PREFIX}ACTION_PARAMETERS_FILE"
    ActionTimeout = f"{ROBOTO_ENV_VAR_PREFIX}ACTION_TIMEOUT"
    AwsAccessKeyId = "AWS_ACCESS_KEY_ID"  # Not prefixed; picked up by AWS SDK
    AwsSecretAccessKey = "AWS_SECRET_ACCESS_KEY"  # Not prefixed; picked up by AWS SDK
    AwsSessionToken = "AWS_SESSION_TOKEN"  # Not prefixed; picked up by AWS SDK
    DatasetMetadataChangesetFile = (
        f"{ROBOTO_ENV_VAR_PREFIX}DATASET_METADATA_CHANGESET_FILE"
    )
    InputDir = f"{ROBOTO_ENV_VAR_PREFIX}INPUT_DIR"
    InvocationId = f"{ROBOTO_ENV_VAR_PREFIX}INVOCATION_ID"
    OrgId = f"{ROBOTO_ENV_VAR_PREFIX}ORG_ID"
    OutputDir = f"{ROBOTO_ENV_VAR_PREFIX}OUTPUT_DIR"
    RobotoServiceUrl = f"{ROBOTO_ENV_VAR_PREFIX}SERVICE_URL"
