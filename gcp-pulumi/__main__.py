import os
import pulumi
import pulumi_gcp as gcp
import pulumi_github as github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Mirror the Github Registry
repo = github.Repository("aurora-humans-app",
    description="Streamlit Application for Uploading Aurora Photos",
    visibility="public"
)

# 2. Push to Container Registry
container_registry = gcp.container.Registry("aurora-humans-container",
    project=os.getenv("GCP_PROJECT_ID")
)

# 3. Google Build
build_trigger = gcp.cloudbuild.Trigger("build-aurora-humans",
    filename="cloudbuild.yaml",
    project=os.getenv("GCP_PROJECT_ID"),
    trigger_template=gcp.cloudbuild.TriggerTriggerTemplateArgs(
        branch_name="main",
        repo_name=repo.name,
    )
)

# 4. Google Run - Deploy the built image to Cloud Run
cloud_run_service = gcp.cloudrun.Service("aurora-humans-app",
    location="asia",
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=container_registry.id.apply(lambda id: f"gcr.io/{os.getenv('GCP_PROJECT_ID')}/my-app:latest")
            )]
        )
    )
)

# 5. Google Deploy with 2 stages - setting up a Delivery Pipeline
delivery_pipeline = gcp.clouddeploy.DeliveryPipeline("aurora-delivery-pipeline",
    location="asia",
    name="aurora-delivery-pipeline",
    project=os.getenv("GCP_PROJECT_ID"),
    serial_pipeline=gcp.clouddeploy.DeliveryPipelineSerialPipelineArgs(
        stages=[
            gcp.clouddeploy.DeliveryPipelineSerialPipelineStageArgs(
                target_id="development"
            ),
            gcp.clouddeploy.DeliveryPipelineSerialPipelineStageArgs(
                target_id="production"
            ),
        ],
    )
)

# 6. Create API Gateway - expose Cloud Run services
api_gw = gcp.apigateway.Api("api_gw", api_id="my-api")
api_gw_api_config = gcp.apigateway.ApiConfig("api_gw_api_config",
    api=api_gw.api_id,
    api_config_id="my-config",
    openapi_documents=[gcp.apigateway.ApiConfigOpenapiDocumentArgs(
        document=gcp.apigateway.ApiConfigOpenapiDocumentDocumentArgs(
            path="spec.yaml",
            contents=pulumi.AssetArchive({
                "spec.yaml": pulumi.FileAsset("path/to/openapi.yaml")
            })
        ),
    )]
)

api_gw_gateway = gcp.apigateway.Gateway("api_gw_gateway",
    api_config=api_gw_api_config.id,
    gateway_id="aurora-gateway"
)

api_gateway = gcp.apigateway.Api("aurora-gateway",
    project=os.getenv("GCP_PROJECT_ID"),
    api_id="aurora-human-api"
)

# Outputs
pulumi.export('repo_name', repo.name)
pulumi.export("container_registry_name", container_registry.id)
pulumi.export("cloud_run_service_url", cloud_run_service.statuses[0].url)
pulumi.export("delivery_pipeline_name", delivery_pipeline.id)
pulumi.export("api_gateway_endpoint", api_gw_gateway.default_hostname)
