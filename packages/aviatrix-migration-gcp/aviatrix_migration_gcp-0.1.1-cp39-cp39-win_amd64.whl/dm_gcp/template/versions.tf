terraform {
  required_providers {
    aviatrix = {
      source  = "aviatrixsystems/aviatrix"
      version = "{{data.aviatrix_provider}}"
    }
    # aws = {
    #   source  = "hashicorp/aws"
    #   version = "{{data.aws_provider}}"
    # }
  }
  required_version = "{{data.terraform_version}}"
}
