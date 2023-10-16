from pathlib import Path
from posixpath import join
from typing import Any, Callable, Dict, List, Optional, Union

from pydantic import UUID4, BaseModel, HttpUrl, SecretStr
from requests import get, post, put

from promptquality.constants.routes import Routes
from promptquality.types.rows import GetRowsRequest
from promptquality.types.run import (
    CreateIntegrationRequest,
    CreateJobRequest,
    CreateProjectRequest,
    CreateRunRequest,
    CreateTemplateRequest,
    CreateTemplateVersionRequest,
    EstimateCostRequest,
    GetMetricsRequest,
    SelectTemplateVersionRequest,
    UploadDatasetRequest,
)
from promptquality.types.user_submitted_metrics import UserSubmittedMetrics
from promptquality.utils.request import HttpHeaders, make_request


class ApiClient(BaseModel):
    api_url: HttpUrl
    token: SecretStr

    @staticmethod
    def healthcheck(base_url: str) -> bool:
        make_request(get, base_url=base_url, endpoint=Routes.healthcheck)
        return True

    @staticmethod
    def username_login(base_url: str, username: str, password: str) -> Dict[str, str]:
        return make_request(
            post,
            base_url=base_url,
            endpoint=Routes.login,
            data={
                "username": username,
                "password": password,
                "auth_method": "email",
            },
        )

    @property
    def base_url(self) -> str:
        return self.api_url.unicode_string()

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token.get_secret_value()}"}

    def _make_request(
        self,
        request_method: Callable,
        endpoint: str,
        body: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        timeout: Union[int, None] = None,
        json_request_only: bool = False,
    ) -> Any:
        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        return make_request(
            request_method=request_method,
            base_url=self.base_url,
            endpoint=endpoint,
            body=body,
            data=data,
            files=files,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    def get_current_user(self) -> Dict[str, str]:
        return self._make_request(get, endpoint=Routes.current_user)

    def get_projects(self) -> List[Dict[str, str]]:
        return self._make_request(get, endpoint=Routes.all_projects)

    def create_project(self, project_request: CreateProjectRequest) -> Dict[str, str]:
        return self._make_request(
            post,
            endpoint=Routes.projects,
            body=project_request.model_dump(),
        )

    def create_template(
        self, template_request: CreateTemplateRequest
    ) -> Dict[str, str]:
        return self._make_request(
            post,
            endpoint=Routes.templates.format(project_id=template_request.project_id),
            body=template_request.model_dump(mode="json"),
        )

    def get_template(self, project_id: UUID4, template_id: UUID4) -> Dict[str, str]:
        return self._make_request(
            get,
            endpoint=Routes.template.format(
                project_id=project_id, template_id=template_id
            ),
        )

    def get_templates(self, project_id: UUID4) -> List[Dict[str, str]]:
        return self._make_request(
            get,
            endpoint=Routes.templates.format(project_id=project_id),
        )

    def create_template_version(
        self,
        template_version_request: CreateTemplateVersionRequest,
    ) -> Dict[str, str]:
        return self._make_request(
            post,
            endpoint=Routes.versions.format(
                project_id=template_version_request.project_id,
                template_id=template_version_request.template_id,
            ),
            body=template_version_request.model_dump(mode="json", exclude_none=True),
        )

    def upload_dataset(self, dataset_request: UploadDatasetRequest) -> Dict[str, str]:
        return self._make_request(
            post,
            json_request_only=True,
            endpoint=Routes.dataset.format(project_id=dataset_request.project_id),
            params=dataset_request.params,
            files=dataset_request.files,
        )

    def create_run(self, run_request: CreateRunRequest) -> Dict[str, str]:
        return self._make_request(
            post,
            endpoint=Routes.runs.format(project_id=run_request.project_id),
            body=run_request.model_dump(mode="json"),
        )

    def create_job(self, job_request: CreateJobRequest) -> Dict[str, str]:
        return self._make_request(
            post,
            endpoint=Routes.jobs,
            body=job_request.model_dump(mode="json", exclude_none=True),
        )

    def get_metrics(self, metrics_request: GetMetricsRequest) -> List[Dict[str, Any]]:
        return self._make_request(
            get,
            endpoint=Routes.metrics.format(**metrics_request.model_dump(mode="json")),
        )

    def get_rows(self, request: GetRowsRequest) -> List[Dict[str, Any]]:
        return self._make_request(
            get,
            endpoint=Routes.rows.format(**request.model_dump(mode="json")),
            params=request.params(),
        )

    def get_estimated_cost(self, cost_request: EstimateCostRequest) -> Dict[str, float]:
        return self._make_request(
            post,
            json_request_only=True,
            endpoint=Routes.cost.format(project_id=cost_request.project_id),
            params=cost_request.params,
            files=cost_request.files,
        )

    def get_job_status(self, job_id: UUID4) -> Dict[str, Any]:
        return self._make_request(get, endpoint=join(Routes.jobs, str(job_id)))

    def put_integration(
        self, integration_request: CreateIntegrationRequest
    ) -> Dict[str, Any]:
        return self._make_request(
            put,
            endpoint=Routes.integrations.format(
                integration_name=integration_request.name
            ),
            body=integration_request.body,
        )

    def put_template_version_selection(
        self, select_version: SelectTemplateVersionRequest
    ) -> Dict[str, Any]:
        return self._make_request(
            put,
            endpoint=Routes.version.format(
                project_id=select_version.project_id,
                template_id=select_version.template_id,
                version=select_version.version,
            ),
        )

    def put_user_metrics(
        self, scores: UserSubmittedMetrics, project_id: UUID4, run_id: UUID4
    ) -> Dict[str, Any]:
        payload = scores.model_dump(mode="json", by_alias=True)
        return self._make_request(
            put,
            endpoint=Routes.user_submitted_metrics.format(
                project_id=project_id, run_id=run_id
            ),
            body=payload,
        )

    def register_scorer(self, scorer_name: str, scorer_file: Path) -> Dict[str, Any]:
        return self._make_request(
            put,
            endpoint=Routes.registered_scorer,
            params=dict(name=scorer_name),
            files=dict(file=scorer_file.open("rb")),
            json_request_only=True,
        )

    def list_registered_scorers(self) -> List[Dict[str, Any]]:
        return self._make_request(get, endpoint=Routes.registered_scorer)
