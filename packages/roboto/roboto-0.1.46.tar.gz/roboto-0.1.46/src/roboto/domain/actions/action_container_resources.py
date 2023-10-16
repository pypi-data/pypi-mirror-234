import collections.abc
import enum
import typing

import pydantic


class ExecutorContainer(enum.Enum):
    LogRouter = "firelens_log_router"
    Monitor = "monitor"
    Setup = "setup"
    Action = "action"
    OutputHandler = "output_handler"


class ComputeRequirements(pydantic.BaseModel):
    """
    Compute requirements for an action invocation.

    .. _Relevant AWS Fargate documentation:
        https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html#fargate-tasks-size
    """

    vCPU: int = 512  # 256, 512, 1024, 2048, 4096, 8192, 16384
    memory: int = 1024  # 512, 1024, 2024, ... (120 * 1024) in MiB
    gpu: typing.Literal[False] = False  # Not yet supported
    storage: int = pydantic.Field(default=21, ge=21, le=200)  # in GiB (min 21, max 200)

    @pydantic.root_validator
    def validate_vcpu_mem_combination(cls, values: dict) -> dict:
        v_cpu = values["vCPU"]
        allowed_vpcu = (256, 512, 1024, 2048, 4096, 8192, 16384)
        if v_cpu not in allowed_vpcu:
            raise ValueError(f"Unsupported vCPU value. Allowed options: {allowed_vpcu}")

        memory = values["memory"]
        allowed_memory: collections.abc.Sequence = list()
        if v_cpu == 256:
            allowed_memory = [512, 1024, 2048]
        elif v_cpu == 512:
            allowed_memory = range(1024, 5 * 1024, 1024)
        elif v_cpu == 1024:
            allowed_memory = range(2 * 1024, 9 * 1024, 1024)
        elif v_cpu == 2048:
            allowed_memory = range(4 * 1024, 17 * 1024, 1024)
        elif v_cpu == 4096:
            allowed_memory = range(8 * 1024, 31 * 1024, 1024)
        elif v_cpu == 8192:
            allowed_memory = range(16 * 1024, 61 * 1024, 4 * 1024)
        elif v_cpu == 16384:
            allowed_memory = range(32 * 1024, 121 * 1024, 8 * 1024)
        else:
            raise ValueError(f"Unknown vCPU value {v_cpu}")

        if memory not in allowed_memory:
            raise ValueError(
                f"Unsupported memory/vCPU combination, allowed memory for {v_cpu} vCPU: {list(allowed_memory)}"
            )

        return values

    class Config:
        extra = "forbid"


class ContainerParameters(pydantic.BaseModel):
    command: typing.Optional[list[str]] = None
    entry_point: typing.Optional[list[str]] = None
    env_vars: typing.Optional[dict[str, str]] = None
    workdir: typing.Optional[str] = None

    class Config:
        extra = "forbid"
