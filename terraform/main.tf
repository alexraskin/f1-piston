terraform {
  backend "s3" {
    bucket  = "terraform-088966585880-us-west-2"
    key     = "f1-piston/terraform.tfstate"
    encrypt = true
    region  = "us-west-2"
    profile = "personal"
  }
}


locals {
  app_name              = "f1-piston"
  aws_region            = "us-west-1"
  service_port          = 8501
  auto_scaling_max_size = 2
}


resource "aws_ecr_repository" "streamlit_ecr" {
  name                 = "streamlit-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

module "app_runner_service" {
  source                = "git@github.com:alexraskin/terraform-aws-app-runner.git?ref=01d070a471ea69e17caeb820283b546a31a0dc88"
  app_name              = local.app_name
  aws_region            = local.aws_region
  ecr_repository_url    = resource.aws_ecr_repository.streamlit_ecr.repository_url
  tags                  = {}
  service_port          = local.service_port
  auto_scaling_max_size = local.auto_scaling_max_size
  environment_variables = {}
  service_memory        = 4096
  service_cpu           = 2048
}
