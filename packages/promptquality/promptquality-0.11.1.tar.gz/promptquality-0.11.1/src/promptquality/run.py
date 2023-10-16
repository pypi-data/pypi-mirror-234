from typing import List, Optional, Union

from promptquality.constants.scorers import Scorers
from promptquality.get_metrics import get_metrics
from promptquality.helpers import (
    create_job,
    create_project,
    create_run,
    create_template,
    upload_custom_metrics,
    upload_dataset,
)
from promptquality.job_progress import job_progress
from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.custom_scorer import CustomScorer
from promptquality.types.registered_scorers import RegisteredScorer
from promptquality.types.run import PromptMetrics
from promptquality.types.settings import Settings
from promptquality.utils.dataset import DatasetType
from promptquality.utils.name import ts_run_name
from promptquality.utils.scorer import bifurcate_scorers


def run(
    template: str,
    dataset: DatasetType,
    project_name: Optional[str] = None,
    run_name: Optional[str] = None,
    template_name: Optional[str] = None,
    scorers: Optional[List[Union[Scorers, CustomScorer, RegisteredScorer, str]]] = None,
    settings: Optional[Settings] = None,
    wait: bool = True,
    silent: bool = False,
    config: Optional[Config] = None,
) -> Optional[PromptMetrics]:
    """
    Create a prompt run.

    This function creates a prompt run that can be viewed on the Galileo console. The
    processing of the prompt run is asynchronous, so the function will return
    immediately. If the `wait` parameter is set to `True`, the function will block
    until the prompt run is complete.

    Additionally, all of the scorers are executed asynchronously in the background after
    the prompt run is complete, regardless of the value of the `wait` parameter.

    Parameters
    ----------
    template : str
        Template text to use for the prompt run.
    dataset : DatasetType
        Dataset to use for the prompt run.
    project_name : Optional[str], optional
        Project name to use, by default None which translates to a randomly generated
        name.
    run_name : Optional[str], optional
        Run name to use, by default None which translates to one derived from the
        project name, current timestamp and template version.
    template_name : Optional[str], optional
        Template name to use, by default None which translates to the project name.
    scorers : List[Union[Scorers, CustomScorer, RegisteredScorer, str]], optional
        List of scorers to use, by default None.
    settings : Optional[Settings], optional
        Settings to use, by default None which translates to the default settings.
    wait : bool, optional
        Whether to wait for the prompt run to complete, by default True.
    silent : bool, optional
        Whether to suppress the console output, by default False.
    config : Optional[Config], optional
        Config to use, by default None which translates to the config being set
        automatically.

    Returns
    -------
    Optional[PromptMetrics]
        Metrics for the prompt run. These are only returned if the `wait` parameter is
        `True` for metrics that have been computed upto that point. Other metrics will
        be computed asynchronously.
    """
    config = config or set_config()
    # Create project.
    project = create_project(project_name, config)
    # Create template.
    template_response = create_template(
        template,
        project.id,
        # Use project name as template name if not provided.
        template_name=template_name or project.name,
        config=config,
    )
    # Upload dataset.
    dataset_id = upload_dataset(
        dataset,
        project.id,
        template_response.selected_version_id,
        config,
    )
    # Run prompt.
    run_id = create_run(
        project.id,
        run_name=run_name
        or ts_run_name(
            template_response.name, template_response.selected_version.version
        ),
        config=config,
    )
    galileo_scorers, custom_scorers, registered_scorers = bifurcate_scorers(scorers)
    job_id = create_job(
        project.id,
        run_id,
        dataset_id,
        template_response.selected_version_id,
        settings,
        galileo_scorers,
        registered_scorers,
        config,
    )
    if wait:
        job_progress(job_id, config)
    if not silent:
        print(f"🔭 View your prompt run on the Galileo console at: {config.run_url}")
    if custom_scorers:
        for scorer in custom_scorers:
            upload_custom_metrics(
                scorer, project_id=project.id, run_id=run_id, config=config
            )
    return get_metrics(
        project_id=project.id, run_id=run_id, job_id=job_id, config=config
    )
