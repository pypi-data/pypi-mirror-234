from typing import Callable, Dict, List, Optional, Union

from pydantic import BaseModel

from promptquality.types.rows import PromptRow

CustomMetricType = Union[float, int, bool, str, None]


class CustomScorer(BaseModel):
    name: str
    executor: Callable[[PromptRow], CustomMetricType]
    aggregator: Optional[
        Callable[[List[CustomMetricType], List[int]], Dict[str, CustomMetricType]]
    ] = None
