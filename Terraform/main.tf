module "cloud_run" { 
  source                = "git@github.ford.com:gcp/tfm-cloud-run.git"
  gcp_project_id        = "ford-ff2caa6b9fe570105b2da7f7" # The id of the project where the cloud run service is to be deployed" 
  service_name          = "test-fa"      # The name of the cloud run service" 
  service_image_url     = "us-central1-docker.pkg.dev/ford-ff2caa6b9fe570105b2da7f7/ford-container-images/ai-agents:v5" 
  gcp_region            = "us-central1" 
  service_account_email = "sa-astro-agent-cr-sb@ford-ff2caa6b9fe570105b2da7f7.iam.gserviceaccount.com"                                                                     # This service account represents the identity of the service and determines what permissions the service has. 
  service_invoker       = ["allUsers"]
  service_vpc_connector = "projects/prj-pp-gen-preprod-net-acc7/locations/us-central1/connectors/preprod-gen-central1"            # See variables.tf for valid options 
  # container_port        = "8080"  
  timeout_seconds       = 3600
  # apigee_environment    = "DEV"   
  cpu_count             = 2 
  min_instance_count    = 1 
  # max_instance_count    = 50 
  memory_size           = 4000
} 
