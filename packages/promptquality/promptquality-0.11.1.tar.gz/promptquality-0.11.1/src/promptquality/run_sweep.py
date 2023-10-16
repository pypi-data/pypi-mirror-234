from itertools import product
from typing import List, Optional, Union

from tqdm.auto import tqdm

from promptquality.constants.models import SupportedModels
from promptquality.constants.scorers import Scorers
from promptquality.helpers import create_project, get_estimated_cost
from promptquality.run import run
from promptquality.set_config import set_config
from promptquality.types.custom_scorer import CustomScorer
from promptquality.types.registered_scorers import RegisteredScorer
from promptquality.types.settings import Settings
from promptquality.utils.dataset import DatasetType


def create_settings_combinations(
    model_aliases: Optional[List[Union[str, SupportedModels]]] = None,
    temperatures: Optional[List[float]] = None,
    max_token_options: Optional[List[int]] = None,
) -> List[Settings]:
    # Create all combinations of settings objects.
    alias_options: List[Optional[str]] = (
        list(model_aliases) if model_aliases else [None]
    )
    temperature_options: List[Optional[float]] = (
        list(temperatures) if temperatures else [None]
    )
    token_options: List[Optional[int]] = (
        list(max_token_options) if max_token_options else [None]
    )
    return [
        Settings(model_alias=alias, temperature=temperature, max_tokens=tokens)
        for alias, temperature, tokens in product(
            alias_options, temperature_options, token_options
        )
    ]


def run_sweep(
    templates: List[str],
    dataset: DatasetType,
    project_name: Optional[str] = None,
    model_aliases: Optional[List[Union[str, SupportedModels]]] = None,
    temperatures: Optional[List[float]] = None,
    max_token_options: Optional[List[int]] = None,
    scorers: Optional[List[Union[Scorers, CustomScorer, RegisteredScorer, str]]] = None,
    execute: bool = False,
    wait: bool = True,
    silent: bool = True,
) -> None:
    """Run a sweep of prompt runs over various settings."""
    config = set_config()
    # Create project.
    project = create_project(project_name, config)

    # Estimate cost.
    estimated_costs = []
    all_settings = create_settings_combinations(
        model_aliases, temperatures, max_token_options
    )
    all_combinations = list(product(templates, all_settings))
    for template, settings in all_combinations:
        estimated_costs.append(
            get_estimated_cost(
                dataset=dataset,
                template=template,
                settings=settings,
                project_id=project.id,
                config=config,
            )
        )
    print(
        f"Estimated total cost for {len(estimated_costs)} runs: "
        f"${sum(estimated_costs)}."
    )
    if not execute:
        print(
            "If you want to execute this run, invoke this function again with "
            "`execute=True`."
        )
    else:
        print(f"Running batch with {len(all_combinations)} runs...")
        for template, settings in tqdm(all_combinations):
            run(
                template=template,
                dataset=dataset,
                project_name=project.name,
                settings=settings,
                scorers=scorers,
                config=config,
                wait=wait,
                silent=silent,
            )
        print(
            "🔭 Batch runs created! View your prompt runs on the Galileo console at: "
            f" {config.project_url}."
        )
