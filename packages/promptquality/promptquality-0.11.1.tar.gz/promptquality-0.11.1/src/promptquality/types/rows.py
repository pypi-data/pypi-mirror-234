from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field

from promptquality.types.pagination import (
    PaginationRequestMixin,
    PaginationResponseMixin,
)


class GetRowsRequest(PaginationRequestMixin):
    project_id: UUID4
    run_id: UUID4

    def params(self) -> Dict[str, Any]:
        """
        Params to be passed to the API request.

        These are primarily the pagination parameters.

        Returns
        -------
        Dict[str, Any]
            Params to be passed to the API request.
        """
        return self.model_dump(mode="json", exclude={"project_id", "run_id"})


class Metrics(BaseModel):
    hallucination: Optional[float] = None
    bleu: Optional[float] = None
    rouge: Optional[float] = None
    pii: Optional[List[str]] = Field(default_factory=list)
    like_dislike: Optional[bool] = None
    toxicity: Optional[float] = None
    factuality: Optional[float] = None
    groundedness: Optional[float] = None
    latency: Optional[float] = None
    context_relevance: Optional[float] = None

    model_config = ConfigDict(extra="allow")


class PromptRow(BaseModel):
    index: int
    prompt: Optional[str] = None
    response: Optional[str] = None
    target: Optional[str] = None
    inputs: Dict[str, Optional[Any]] = Field(default_factory=dict)
    hallucination: Optional[float] = None
    bleu: Optional[float] = None
    rouge: Optional[float] = None
    cost: Optional[float] = None
    like_dislike: Optional[bool] = None
    metrics: Metrics = Field(default_factory=Metrics)

    model_config = ConfigDict(extra="allow")


class PromptRows(PaginationResponseMixin):
    rows: List[PromptRow] = Field(default_factory=list)
