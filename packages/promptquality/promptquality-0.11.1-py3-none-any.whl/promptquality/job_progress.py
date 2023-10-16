from random import random
from time import sleep
from typing import Optional

from pydantic import UUID4
from tqdm.auto import tqdm

from promptquality.constants.job import JobStatus
from promptquality.helpers import get_job_status
from promptquality.types.config import Config
from promptquality.utils.logger import logger


def job_progress(
    job_id: Optional[UUID4] = None, config: Optional[Config] = None
) -> UUID4:
    backoff = random()
    job_status = get_job_status(job_id, config)
    job_progress_bar = tqdm(
        total=job_status.steps_total,
        position=0,
        leave=True,
        desc=job_status.progress_message,
    )
    while job_status.status in [JobStatus.unstarted, JobStatus.in_progress]:
        sleep(backoff)
        job_status = get_job_status(job_id, config)
        job_progress_bar.set_description(job_status.progress_message)
        job_progress_bar.update(job_status.steps_completed - job_progress_bar.n)
        backoff = random()
    job_progress_bar.close()
    logger.debug(f"Job {job_id} status: {job_status.status}.")
    return job_status.id
