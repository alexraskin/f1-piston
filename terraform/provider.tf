terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.34"
    }
  }
}

provider "aws" {
  profile = "personal"
  region  = "us-west-2"
  default_tags {
    tags = {
      Name = "f1-piston"
    }
  }
}