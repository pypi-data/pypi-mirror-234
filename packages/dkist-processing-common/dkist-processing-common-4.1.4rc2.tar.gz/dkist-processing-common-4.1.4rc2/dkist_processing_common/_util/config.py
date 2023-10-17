"""Common configurations."""
from dkist_service_configuration import MeshServiceConfigurationBase
from dkist_service_configuration.settings import DEFAULT_MESH_SERVICE
from dkist_service_configuration.settings import MeshService
from pydantic import BaseModel
from pydantic import Field


class RetryConfig(BaseModel):
    """Retry metadata model."""

    retry_delay: int = 1
    retry_backoff: int = 2
    retry_jitter: tuple[int, int] = (1, 10)
    retry_max_delay: int = 300
    retry_tries: int = -1


class ServiceConfiguration(MeshServiceConfigurationBase):
    """Common configurations."""

    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    # interservice bus
    isb_username: str = "guest"
    isb_password: str = "guest"
    isb_exchange: str = "master.direct.x"
    isb_heartbeat_timeout: int = 60  # 1 minute
    # metadata-store-api
    gql_auth_token: str | None = None
    # object-store-api
    object_store_access_key: str | None = None
    object_store_secret_key: str | None = None
    object_store_use_ssl: bool = False
    # start object-clerk library
    multipart_threshold: int | None = None
    s3_client_config: dict | None = None
    s3_upload_config: dict | None = None
    s3_download_config: dict | None = None
    # globus
    globus_transport_params: dict = Field(default_factory=dict)
    globus_client_id: str | None = None
    globus_client_secret: str | None = None
    object_store_endpoint: str | None = None
    scratch_endpoint: str | None = None
    # scratch
    scratch_base_path: str = Field(default="scratch/")
    # docs
    docs_base_url: str = Field(default="my_test_url")

    @property
    def metadata_store_api_base(self) -> str:
        """Metadata store api url."""
        gateway = self.service_mesh_detail(service_name="internal-api-gateway")
        return f"http://{gateway.host}:{gateway.port}/graphql"

    @property
    def isb_mesh_service(self) -> MeshService:
        """Interservice bus host and port."""
        return self.service_mesh_detail(service_name="interservice-bus")

    @property
    def object_store_api_mesh_service(self) -> MeshService:
        """Object store host and port."""
        return self.service_mesh_detail(service_name="object-store-api")

    @property
    def scratch_inventory_mesh_service(self) -> MeshService:
        """Scratch inventory host and port."""
        mesh = self.service_mesh_detail(service_name="automated-processing-scratch-inventory")
        if mesh == DEFAULT_MESH_SERVICE:
            return MeshService(mesh_address="localhost", mesh_port=6379)  # testing default
        return mesh


service_configuration = ServiceConfiguration()
service_configuration.log_configurations()
