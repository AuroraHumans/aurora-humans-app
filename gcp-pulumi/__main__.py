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
repo = github.Repository("AuroraHumans/aurora-humans-app",
    name="Aurora-Humans",
    description="Streamlit Application for Uploading Aurora Photos",
    visibility="public"
)

# 2. Push to Container Registry
# Making use of GCP's Container Registry - this step would be a result of your build & push in Cloud Build
container_registry = gcp.container.Registry("core-apps",
    project=os.getenv("GCP_PROJECT_ID")
)

# 3. Google Build
# Set up Cloud Build trigger to automate the build and push steps
build_trigger = gcp.cloudbuild.Trigger("build-aurora-humans",
    filename="cloudbuild.yaml",
    project=os.getenv("GCP_PROJECT_ID"),
    trigger_template=gcp.cloudbuild.TriggerTriggerTemplateArgs(
        branch_name="main",
        repo_name=repo.name,
    )
)

# 4. Google Run - Deploy the built image to Cloud Run
cloud_run_service = gcp.cloudrun.Service("aurora-humans-run",
    location="asia",
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=container_registry.id.apply(lambda id: f"gcr.io/{id}/my-app:latest")
            )]
        )
    ))

# 5. Google Deploy with 2 stages - setting up a Delivery Pipeline
delivery_pipeline = gcp.clouddeploy.DeliveryPipeline(resource_name="aurora-deliver-pipeline", location="asia", name="aurora-deliver-pipeline",
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
api_gateway = gcp.apigateway.Api("aurora-gateway",
    project=os.getenv("GCP_PROJECT_ID"),
    api_id="aurora-human-api",
)

# Outputs
pulumi.export("repository_url", repo.clone_url)
pulumi.export("container_registry_name", container_registry.id)
pulumi.export("cloud_run_service_url", cloud_run_service.statuses[0].url)
pulumi.export("delivery_pipeline_name", delivery_pipeline.id)
pulumi.export("api_gateway_service_endpoint", api_gateway.discovery_endpoint)
