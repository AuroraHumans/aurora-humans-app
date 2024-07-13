gcloud projects add-iam-policy-binding langchaindata \
    --member="serviceAccount:deploy-service-account@langchaindata.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding langchaindata \
    --member="serviceAccount:deploy-service-account@langchaindata.iam.gserviceaccount.com" \
    --role="roles/run.admin"

