from io import BufferedReader
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)

from promptquality.constants.dataset_format import DatasetFormat
from promptquality.constants.integrations import IntegrationName
from promptquality.constants.run import RunDefaults
from promptquality.constants.scorers import Scorers
from promptquality.types.registered_scorers import RegisteredScorer
from promptquality.types.settings import Settings
from promptquality.utils.dataset import parse_dataset
from promptquality.utils.name import random_name


class RandomName(BaseModel):
    name: str = Field(default_factory=random_name)

    @field_validator("name", mode="before")
    def set_name(cls, value: Optional[str]) -> str:
        if value is None:
            return random_name()
        return value


class CreateProjectRequest(RandomName):
    type: str = RunDefaults.project_type


class CreateProjectResponse(CreateProjectRequest):
    id: UUID4


class BaseTemplateVersionRequest(BaseModel):
    template: str
    version: Optional[int] = None


class CreateTemplateRequest(RandomName, BaseTemplateVersionRequest):
    project_id: UUID4


class CreateTemplateVersionRequest(BaseTemplateVersionRequest):
    template_id: UUID4
    project_id: UUID4


class BaseTemplateVersionResponse(BaseTemplateVersionRequest):
    id: UUID4


class CreateTemplateVersionResponse(BaseTemplateVersionResponse):
    version: int


class BaseTemplateResponse(RandomName):
    id: UUID4
    template: str
    selected_version: CreateTemplateVersionResponse
    selected_version_id: UUID4
    all_versions: List[CreateTemplateVersionResponse] = Field(default_factory=list)


class BaseDatasetRequest(BaseModel):
    format: DatasetFormat = DatasetFormat.csv
    file_path: Path = Field(exclude=True)

    @model_validator(mode="before")
    def dataset_to_path(cls, values: Dict) -> Dict:
        if "file_path" in values:
            values["file_path"], values["format"] = parse_dataset(values["file_path"])
        return values

    @property
    def files(self) -> Dict[str, BufferedReader]:
        return dict(file=self.file_path.open("rb"))


class UploadDatasetRequest(BaseDatasetRequest):
    project_id: UUID4
    prompt_template_version_id: UUID4
    file_path: Path = Field(exclude=True)

    @property
    def params(self) -> Dict[str, str]:
        return dict(
            prompt_template_version_id=str(self.prompt_template_version_id),
            format=self.format.value,
        )


class UploadDatasetResponse(BaseModel):
    id: UUID4 = Field(alias="dataset_id")


class EstimateCostRequest(BaseDatasetRequest, Settings):
    project_id: UUID4 = Field(exclude=True)
    template: str = Field(serialization_alias="prompt_template")

    @property
    def params(self) -> Dict[str, str]:
        return self.model_dump(
            mode="json", by_alias=True, exclude_unset=True, exclude_none=True
        )


class EstimatedCostResponse(BaseModel):
    total_cost: float
    query_cost: float
    log_probs_cost: float


class CreateRunRequest(RandomName):
    project_id: UUID4
    task_type: int = RunDefaults.task_type


class CreateRunResponse(CreateRunRequest):
    id: UUID4


class ScorersConfiguration(BaseModel):
    toxicity: bool = False
    factuality: bool = False
    groundedness: bool = False
    context_relevance: bool = False
    latency: bool = True
    sexist: bool = False

    # PII fields.
    ssn: bool = False
    credit_card: bool = False
    email: bool = False
    phone: bool = False
    street_address: bool = False

    @classmethod
    def from_scorers(cls, scorers: List[Scorers]) -> "ScorersConfiguration":
        config = cls(**{scorer.value: True for scorer in scorers})
        if "pii" in scorers:
            config.ssn = True
            config.credit_card = True
            config.email = True
            config.phone = True
            config.street_address = True
        return config


class CreateJobRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4
    prompt_dataset_id: UUID4
    prompt_template_version_id: UUID4
    prompt_settings: Optional[Settings] = None
    prompt_scorers_configuration: Optional[ScorersConfiguration] = None
    prompt_registered_scorers_configuration: Optional[List[RegisteredScorer]] = None
    job_name: str = RunDefaults.job_name
    task_type: int = RunDefaults.task_type


class CreateJobResponse(CreateJobRequest):
    id: UUID4 = Field(alias="job_id")


class GetMetricsRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4


class PromptMetrics(BaseModel):
    total_responses: Optional[int] = None
    average_hallucination: Optional[float] = None
    average_bleu: Optional[float] = None
    average_rouge: Optional[float] = None
    average_cost: Optional[float] = None
    total_cost: Optional[float] = None

    model_config = ConfigDict(extra="allow")


class GetJobStatusResponse(BaseModel):
    id: UUID4
    project_id: UUID4
    run_id: UUID4
    status: str
    error_message: Optional[str]
    progress_message: Optional[str]
    steps_completed: int = 0
    steps_total: int = 0
    progress_percent: float = 0.0


class CreateIntegrationRequest(BaseModel):
    api_key: SecretStr
    name: IntegrationName = Field(default=IntegrationName.openai)
    organization_id: Optional[str] = None

    @property
    def body(self) -> Dict[str, Any]:
        extra = (
            dict(organization_id=self.organization_id)
            if self.organization_id
            else dict()
        )
        return dict(token=self.api_key.get_secret_value(), extra=extra)


class SelectTemplateVersionRequest(BaseModel):
    project_id: UUID4
    template_id: UUID4
    version: int


class UserSubmittedMetricsResponse(BaseModel):
    project_id: UUID4
    run_id: UUID4
    job_id: UUID4
    scorer_name: str
