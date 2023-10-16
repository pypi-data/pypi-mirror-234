from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from promptquality.constants.models import SupportedModels


class Settings(BaseModel):
    """Settings for a prompt run that a user can configure."""

    model_alias: Optional[SupportedModels] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stop_sequences: Optional[List[str]] = None

    top_p: Optional[int] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None

    # Internal settings.
    logprobs: Optional[int] = None
    n: Optional[int] = None
    deployment_id: Optional[str] = None
    api_type: Optional[str] = None
    api_version: Optional[str] = None

    model_config = ConfigDict(
        # Avoid Pydantic's protected namespace warning since we want to use
        # `model_alias` as a field name.
        protected_namespaces=(),
        # Disallow extra fields.
        extra="allow",
    )
