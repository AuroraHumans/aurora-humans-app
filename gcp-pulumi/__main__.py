"""
The core logic for Pulumi infrastructure management


"""
import os
import pulumi
import pulumi_gcp as gcp
import pulumi_github as github
from dotenv import load_dotenv
load_dotenv()

# 1. Mirror the Github Registry
# Assuming that the GitHub repository already exists
repo = github.Repository("aurora-humans-app",
    description="Streamlit Application for Uploading Aurora Photos",
    visibility="public"
)

# 2. Push to Container Registry
# Making use of GCP's Container Registry - this step would be a result of your build & push in Cloud Build
container_registry = gcp.container.Registry("aurora-humans-container",
    project=os.getenv("GCP_PROJECT_ID")
)

# 3. Google Build
# Set up Cloud Build trigger to automate the build and push steps
'''build_trigger = gcp.cloudbuild.Trigger("build-aurora-humans",
    filename="cloudbuild.yaml",
    project=os.getenv("GCP_PROJECT_ID"),
    trigger_template=gcp.cloudbuild.TriggerTriggerTemplateArgs(
        branch_name="main",
        repo_name=repo.name,
    )
)'''

# 4. Google Run - Deploy the built image to Cloud Run
cloud_run_service = gcp.cloudrun.Service("aurora-humans-app",
    location="asia",
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=container_registry.id.apply(lambda id: f"gcr.io/{id}/my-app:latest")
            )]
        )
    ))

# 5. Google Deploy with 2 stages - setting up a Delivery Pipeline
'''delivery_pipeline = gcp.clouddeploy.DeliveryPipeline(resource_name="aurora-deliver-pipeline", location="asia", name="aurora-deliver-pipeline",
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
)'''

# @TODO IMPLEMENT GATEWAY
'''# 6. Create API Gateway - expose Cloud Run services
import pulumi_std as std

api_gw = gcp.apigateway.Api("api_gw", api_id="my-api")
api_gw_api_config = gcp.apigateway.ApiConfig("api_gw",
    api=api_gw.api_id,
    api_config_id="my-config",
    openapi_documents=[gcp.apigateway.ApiConfigOpenapiDocumentArgs(
        document=gcp.apigateway.ApiConfigOpenapiDocumentDocumentArgs(
            path="spec.yaml",
            contents=std.filebase64(input="test-fixtures/openapi.yaml").result,
        ),
    )])

api_gw_gateway = gcp.apigateway.Gateway("api_gw",
    api_config=api_gw_api_config.id,
    gateway_id="aurora-gateway",
    )

api_gateway = gcp.apigateway.Api("aurora-gateway",
    project=os.getenv("GCP_PROJECT_ID"),
    api_id="aurora-human-api",
    
)'''

# Outputs
pulumi.export('repo_name', repo.name)
pulumi.export("container_registry_name", container_registry.id)
pulumi.export("cloud_run_service_url", cloud_run_service.statuses[0].url)
#pulumi.export("delivery_pipeline_name", delivery_pipeline.id)
#pulumi.export(api_gateway.discovery_endpoint)
