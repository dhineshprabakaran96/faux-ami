module "cloud_run" { 
  source                = "tfregistry.fcp.ford.com/ford/cloud-run/gcp"
  gcp_project_id        = "ford-4360b648e7193d62719765c7" # The id of the project where the cloud run service is to be deployed" 
  service_name          = "test-fa"      # The name of the cloud run service" 
  service_image_url     = "us-central1-docker.pkg.dev/ford-4360b648e7193d62719765c7/ford-container-images/fa-dp:1.0" 
  gcp_region            = "us-central1" 
  service_account_email = "sa-chatgpt-run@ford-4360b648e7193d62719765c7.iam.gserviceaccount.com"                                                                     # This service account represents the identity of the service and determines what permissions the service has. 
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
