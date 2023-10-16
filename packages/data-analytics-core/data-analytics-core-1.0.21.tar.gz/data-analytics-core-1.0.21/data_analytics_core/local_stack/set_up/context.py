import uuid
from dataclasses import dataclass


@dataclass
class TestLambdaContext:
    aws_request_id: uuid.UUID
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = ""

    def __init__(self, function_name: str = "test"):
        self.function_name = function_name
        self.invoked_function_arn: str = (
            "arn:aws:lambda:eu-central-1:111111111111:" f"function:{self.function_name}"
        )
        self.aws_request_id = uuid.uuid1()
