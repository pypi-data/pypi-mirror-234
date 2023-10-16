from typing import Dict, List, Optional

from pydantic import UUID4

from promptquality.constants.scorers import Scorers
from promptquality.get_rows import get_rows
from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.custom_scorer import CustomScorer
from promptquality.types.registered_scorers import RegisteredScorer
from promptquality.types.run import (
    BaseTemplateResponse,
    CreateJobRequest,
    CreateJobResponse,
    CreateProjectRequest,
    CreateProjectResponse,
    CreateRunRequest,
    CreateRunResponse,
    CreateTemplateRequest,
    CreateTemplateVersionRequest,
    CreateTemplateVersionResponse,
    EstimateCostRequest,
    EstimatedCostResponse,
    GetJobStatusResponse,
    ScorersConfiguration,
    SelectTemplateVersionRequest,
    UploadDatasetRequest,
    UploadDatasetResponse,
    UserSubmittedMetricsResponse,
)
from promptquality.types.settings import Settings
from promptquality.types.user_submitted_metrics import UserSubmittedMetrics
from promptquality.utils.dataset import DatasetType
from promptquality.utils.logger import logger


def create_project(
    project_name: Optional[str] = None, config: Optional[Config] = None
) -> CreateProjectResponse:
    config = config or set_config()
    project_request = CreateProjectRequest(name=project_name)
    existing_projects: Dict[str, CreateProjectResponse] = {
        proj.name: proj for proj in get_all_projects(config)
    }
    if project_request.name in existing_projects:
        logger.info(f"Project {project_request.name} already exists, using it.")
        project_response = existing_projects[project_request.name]
    else:
        logger.debug(f"Creating project {project_request.name}...")
        response_dict = config.api_client.create_project(project_request)
        project_response = CreateProjectResponse.model_validate(response_dict)
        logger.debug(
            f"Created project with name {project_response.name}, ID "
            f"{project_response.id}."
        )
    config.merge_project(project_response)
    return project_response


def get_all_projects(config: Optional[Config] = None) -> List[CreateProjectResponse]:
    config = config or set_config()
    logger.debug("Getting all projects...")
    return [
        CreateProjectResponse.model_validate(proj)
        for proj in config.api_client.get_projects()
    ]


def create_template(
    template: str,
    project_id: Optional[UUID4] = None,
    template_name: Optional[str] = None,
    config: Optional[Config] = None,
) -> BaseTemplateResponse:
    """
    Create a template in the project.

    If the project ID is not provided, it will be taken from the config.

    If a template with the same name already exists, it will be used. If the template
    text is the same, the existing template version will be selected. Otherwise, a new
    template version will be created and selected.

    Parameters
    ----------
    template : str
        Template text to use for the new template.
    project_id : Optional[UUID4], optional
        Project ID, by default None, i.e. use the current project ID in config.
    template_name : Optional[str], optional
        Name for the template, by default None, i.e. use a random name.
    config : Optional[Config], optional
        PromptQuality Configuration, by default None, i.e. use the current config on
        disk.

    Returns
    -------
    BaseTemplateResponse
        Validated response from the API.

    Raises
    ------
    ValueError
        If the project ID is not set in config.
    """
    config = config or set_config()
    project_id = project_id or config.current_project_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config to create a template."
        )
    template_request = CreateTemplateRequest(
        template=template, project_id=project_id, name=template_name
    )
    existing_templates = {
        template.name: template for template in get_templates(project_id, config)
    }
    if template_request.name in existing_templates:
        existing_template_response = existing_templates[template_request.name]
        logger.debug(
            f"Template {template_request.name} already exists, using it. "
            f"Template ID is {existing_template_response.id}."
        )
        existing_template_text = {
            template_version.template: template_version
            for template_version in existing_template_response.all_versions
        }
        if template_request.template in existing_template_text:
            logger.debug(
                f"Template text for template {template_request.name} already exists, "
                "selecting it."
            )
            template_version = existing_template_text[template_request.template]
        else:
            logger.debug(
                "Creating template version for template "
                f"{existing_template_response.id}..."
            )
            template_version = create_template_version(
                template_request.template,
                template_id=existing_template_response.id,
                project_id=project_id,
                config=config,
            )
        template_response = select_template_version(
            template_version.version, project_id, existing_template_response.id, config
        )
    else:
        logger.debug(f"Creating template {template_request.name}...")
        response_dict = config.api_client.create_template(template_request)
        template_response = BaseTemplateResponse.model_validate(response_dict)
    config.merge_template(template_response)
    logger.debug(
        f"Created template with name {template_response.name}, ID "
        f"{template_response.id}."
    )
    return template_response


def get_template(
    project_id: Optional[UUID4] = None,
    template_id: Optional[UUID4] = None,
    config: Optional[Config] = None,
) -> BaseTemplateResponse:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    template_id = template_id or config.current_template_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config to get the template."
        )
    if not template_id:
        raise ValueError(
            "Template ID must be provided or set in config to get the template."
        )
    logger.debug(f"Getting template for {project_id=} and {template_id=}...")
    return BaseTemplateResponse.model_validate(
        config.api_client.get_template(project_id=project_id, template_id=template_id)
    )


def get_templates(
    project_id: Optional[UUID4] = None, config: Optional[Config] = None
) -> List[BaseTemplateResponse]:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config to get the templates."
        )
    logger.debug(f"Getting all templates for {project_id=}...")
    return [
        BaseTemplateResponse.model_validate(template)
        for template in config.api_client.get_templates(project_id=project_id)
    ]


def select_template_version(
    version: int,
    project_id: Optional[UUID4] = None,
    template_id: Optional[UUID4] = None,
    config: Optional[Config] = None,
) -> BaseTemplateResponse:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    template_id = template_id or config.current_template_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config to select a different "
            "template version."
        )
    if not template_id:
        raise ValueError(
            "Template ID must be provided or set in config to select a different "
            "template version."
        )

    template_version_request = SelectTemplateVersionRequest(
        project_id=project_id, template_id=template_id, version=version
    )
    logger.debug(
        f"Selecting template version {template_version_request.version} for "
        f"template ID {template_version_request.template_id}..."
    )
    response_dict = config.api_client.put_template_version_selection(
        template_version_request
    )
    template_response = BaseTemplateResponse.model_validate(response_dict)
    config.merge_template(template_response)
    logger.debug(
        f"Selected template version with ID {template_response.selected_version_id}, "
        f"version {template_response.selected_version} for template ID "
        f"{template_response.selected_version_id}."
    )
    return template_response


def create_template_version(
    template: str,
    project_id: Optional[UUID4] = None,
    template_id: Optional[UUID4] = None,
    version: Optional[int] = None,
    config: Optional[Config] = None,
) -> CreateTemplateVersionResponse:
    """
    Create a template version for the current template ID in config.

    Parameters
    ----------
    template : str
        Template text to use for the new template version.
    project_id : Optional[UUID4], optional
        Project ID, by default None, i.e. use the current project ID in config.
    template_id : Optional[UUID4], optional
        Template ID, by default None, i.e. use the current template ID in config.
    version : Optional[int], optional
        Version number, by default None, i.e. use the next version number.
    config : Optional[Config], optional
        PromptQuality Configuration, by default None, i.e. use the current config on
        disk.

    Returns
    -------
    CreateTemplateVersionResponse
        Validated response from the API.

    Raises
    ------
    ValueError
        If the template ID is not set in config.
    ValueError
        If the project ID is not set in config.
    """
    config = config or set_config()
    project_id = project_id or config.current_project_id
    template_id = template_id or config.current_template_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config before creating template "
            "version."
        )
    if not template_id:
        raise ValueError(
            "Template ID must be provided or set in config before creating template "
            "version."
        )
    version_request = CreateTemplateVersionRequest(
        template=template,
        version=version,
        project_id=project_id,
        template_id=template_id,
    )
    logger.debug(
        "Creating template version for template ID " f"{version_request.template_id}..."
    )
    response_dict = config.api_client.create_template_version(version_request)
    version_response = CreateTemplateVersionResponse.model_validate(response_dict)
    config.merge_template_version(version_response)
    logger.debug(
        f"Created template version with ID {version_response.id}, "
        f"version {version_response.version}."
    )
    return version_response


def upload_dataset(
    dataset: DatasetType,
    project_id: UUID4,
    template_version_id: UUID4,
    config: Optional[Config] = None,
) -> UUID4:
    config = config or set_config()
    dataset_request = UploadDatasetRequest(
        project_id=project_id,
        prompt_template_version_id=template_version_id,
        file_path=dataset,
    )
    logger.debug(f"Uploading dataset {dataset_request.file_path}...")
    response_dict = config.api_client.upload_dataset(dataset_request)
    dataset_response = UploadDatasetResponse.model_validate(response_dict)
    config.merge_dataset(dataset_response)
    logger.debug(f"Uploaded dataset with ID {dataset_response.id}.")
    return dataset_response.id


def create_run(
    project_id: UUID4, run_name: Optional[str] = None, config: Optional[Config] = None
) -> UUID4:
    config = config or set_config()
    run_request = CreateRunRequest(name=run_name, project_id=project_id)
    logger.debug(f"Creating run {run_request.name}...")
    response_dict = config.api_client.create_run(run_request)
    run_response = CreateRunResponse.model_validate(response_dict)
    config.merge_run(run_response)
    logger.debug(f"Created run with name {run_request.name}, ID {run_response.id}.")
    return run_response.id


def create_job(
    project_id: Optional[UUID4] = None,
    run_id: Optional[UUID4] = None,
    dataset_id: Optional[UUID4] = None,
    template_version_id: Optional[UUID4] = None,
    settings: Optional[Settings] = None,
    scorers: Optional[List[Scorers]] = None,
    registered_scorers: Optional[List[RegisteredScorer]] = None,
    config: Optional[Config] = None,
) -> UUID4:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    run_id = run_id or config.current_run_id
    dataset_id = dataset_id or config.current_dataset_id
    template_version_id = template_version_id or config.current_template_version_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config before creating job."
        )
    if not run_id:
        raise ValueError(
            "Run ID must be provided or set in config before creating job."
        )
    if not dataset_id:
        raise ValueError(
            "Dataset ID must be provided or set in config before creating job."
        )
    if not template_version_id:
        raise ValueError(
            "Template version ID must be provided or set in config before creating "
            "job."
        )
    job_request = CreateJobRequest(
        project_id=project_id,
        run_id=run_id,
        prompt_dataset_id=dataset_id,
        prompt_settings=settings,
        prompt_scorers_configuration=ScorersConfiguration.from_scorers(scorers)
        if scorers
        else None,
        prompt_registered_scorers_configuration=registered_scorers,
        prompt_template_version_id=template_version_id,
    )
    logger.debug("Creating job...")
    response_dict = config.api_client.create_job(job_request)
    job_response = CreateJobResponse.model_validate(response_dict)
    config.merge_job(job_response)
    logger.debug(f"Created job with ID {job_response.id}.")
    return job_response.id


def get_estimated_cost(
    dataset: DatasetType,
    template: str,
    project_id: Optional[UUID4] = None,
    settings: Optional[Settings] = None,
    config: Optional[Config] = None,
) -> float:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config before estimating cost."
        )
    cost_request = EstimateCostRequest(
        project_id=project_id,
        file_path=dataset,
        template=template,
        **(settings.model_dump() if settings else {}),
    )
    logger.debug("Estimating cost...")
    response_dict = config.api_client.get_estimated_cost(cost_request)
    cost_response = EstimatedCostResponse.model_validate(response_dict)
    logger.debug(f"Estimated cost is {cost_response.total_cost}.")
    return cost_response.total_cost


def get_job_status(
    job_id: Optional[UUID4] = None, config: Optional[Config] = None
) -> GetJobStatusResponse:
    config = config or set_config()
    logger.debug(f"Getting job status for job {job_id}...")
    job_id = job_id or config.current_job_id
    if not job_id:
        raise ValueError("job_id must be provided")
    response_dict = config.api_client.get_job_status(job_id)
    job_status_response = GetJobStatusResponse.model_validate(response_dict)
    logger.debug(
        f"Got job status for job {job_id}, status is "
        f"{job_status_response.progress_message}, "
        f"{job_status_response.progress_percent} percentage."
    )
    return job_status_response


def upload_custom_metrics(
    custom_scorer: CustomScorer,
    project_id: Optional[UUID4] = None,
    run_id: Optional[UUID4] = None,
    config: Optional[Config] = None,
) -> UserSubmittedMetricsResponse:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    run_id = run_id or config.current_run_id
    if not project_id:
        raise ValueError(
            "Project ID must be provided or set in config before uploading custom "
            "metrics."
        )
    if not run_id:
        raise ValueError(
            "Run ID must be provided or set in config before uploading custom "
            "metrics."
        )
    prompt_rows = get_rows(project_id, run_id, config)
    scores = UserSubmittedMetrics.from_scorer(custom_scorer, prompt_rows)
    logger.debug(f"Uploading custom scores for {custom_scorer.name}...")
    response_dict = config.api_client.put_user_metrics(scores, project_id, run_id)
    upload_metrics_response = UserSubmittedMetricsResponse.model_validate(response_dict)
    logger.debug(
        f"Uploaded custom scores for {custom_scorer.name} with job ID "
        f"{upload_metrics_response.job_id}."
    )
    return upload_metrics_response
