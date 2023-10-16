from typing import Optional

from pydantic import SecretStr

from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.run import CreateIntegrationRequest


def add_openai_integration(
    api_key: str, organization_id: Optional[str] = None, config: Optional[Config] = None
) -> None:
    config = config or set_config()
    config.api_client.put_integration(
        CreateIntegrationRequest(
            api_key=SecretStr(api_key), organization_id=organization_id
        )
    )
