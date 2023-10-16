from typing import Any, Optional

from pydantic import BaseModel, field_validator, model_validator, ConfigDict


class DataSource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    s3_url: str
    metadata: Optional[dict[str, Any]]


class ExecutionResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    result: dict[str, DataSource]


class Operation(BaseModel):
    """Formalized `Instruction`."""

    input: list[str]
    output: list[str]
    data_sources: dict[str, DataSource]
    command: str
    args: dict[str, Any]

    @field_validator("input")
    @classmethod
    def validate_input_length(cls, val: list) -> list:
        if len(val) < 1:
            raise ValueError(f"input must have at least one  item.")
        return val

    @field_validator("output")
    @classmethod
    def validate_output_length(cls, val: list) -> list:
        if len(val) != 1:
            raise ValueError(f"Tablegpt-operator must be one and only one output.")
        return val

    @field_validator("data_sources")
    @classmethod
    def validate_data_sources_length(cls, val: dict) -> list:
        if len(val.keys()) < 1:
            raise ValueError(f"data_sources must have at least one 'url' item.")
        return val

    @model_validator(mode="after")
    def validate_model_params(self) -> "Operation":
        if len(self.data_sources.items()) != len(self.input):
            raise ValueError(f"The data_sources length must be equal to input length")
        return self


class SingleOperation(Operation):
    ...


class BatchOperation(BaseModel):
    """Formalized `Instruction`."""

    operations: list[Operation]

    @field_validator("operations")
    @classmethod
    def validate_operations_length(cls, val: list) -> list:
        if len(val) < 1:
            raise ValueError(f"operations must have at least one 'operation' item.")
        return val
