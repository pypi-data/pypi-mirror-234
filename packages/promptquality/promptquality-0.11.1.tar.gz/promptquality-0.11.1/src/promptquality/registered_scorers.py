from pathlib import Path
from typing import List, Optional, Union

from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.registered_scorers import (
    ListRegisteredScorers,
    RegisteredScorer,
)
from promptquality.utils.logger import logger


def register_scorer(
    scorer_name: str, scorer_file: Union[str, Path], config: Optional[Config] = None
) -> RegisteredScorer:
    config = config or set_config()
    scorer_file = Path(scorer_file)
    if not scorer_file.exists():
        raise FileNotFoundError(f"Scorer file {scorer_file} does not exist.")
    response_dict = config.api_client.register_scorer(scorer_name, scorer_file)
    scorer = RegisteredScorer.model_validate(response_dict)
    logger.debug(f"Registered scorer {scorer.name} with id {scorer.id}.")
    return scorer


def list_registered_scorers(config: Optional[Config] = None) -> List[RegisteredScorer]:
    config = config or set_config()
    response_dict = config.api_client.list_registered_scorers()
    scorers = ListRegisteredScorers.model_validate(response_dict)
    logger.debug(f"Found {len(scorers.scorers)} registered scorers.")
    return scorers.scorers
