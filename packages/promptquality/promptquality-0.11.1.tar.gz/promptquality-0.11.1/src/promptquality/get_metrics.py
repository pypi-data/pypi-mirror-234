from typing import Optional

from pydantic import UUID4

from promptquality.constants.job import JobStatus
from promptquality.helpers import get_job_status
from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.run import GetMetricsRequest, PromptMetrics


def get_metrics(
    project_id: Optional[UUID4] = None,
    run_id: Optional[UUID4] = None,
    job_id: Optional[UUID4] = None,
    config: Optional[Config] = None,
) -> Optional[PromptMetrics]:
    config = config or set_config()
    project_id = project_id or config.current_project_id
    run_id = run_id or config.current_run_id
    job_id = job_id or config.current_job_id
    if not project_id:
        raise ValueError("project_id must be provided")
    if not run_id:
        raise ValueError("run_id must be provided")
    if not job_id:
        raise ValueError("job_id must be provided")
    job_status = get_job_status(job_id, config)
    metrics = None
    if job_status.status in [JobStatus.unstarted, JobStatus.in_progress]:
        print("Job is still in progress. Please run pq.get_metrics() again later.")
    elif job_status.status == JobStatus.failed:
        print(f"Job failed with error message {job_status.error_message}.")
    elif job_status.status == JobStatus.completed:
        metrics_request = GetMetricsRequest(project_id=project_id, run_id=run_id)
        all_metrics = config.api_client.get_metrics(metrics_request)
        if all_metrics:
            metrics = PromptMetrics.model_validate(all_metrics[-1]["extra"])
        else:
            print(
                "Job completed, but no metrics found. Please run pq.get_metrics() "
                "again later."
            )
    else:
        raise ValueError(f"Job status {job_status.status} not recognized.")
    return metrics
