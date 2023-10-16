terraform {
  required_providers {
    aviatrix = {
      source = "AviatrixSystems/aviatrix"
      version = "{{data.aviatrix_provider}}"
    }
  }
  required_version = "{{data.terraform_version}}"
}

# provider "aviatrix" {
#   username      = "admin"
#   # password      = data.aws_ssm_parameter.avx-password.value
#   password = "Cisco123!"
#   controller_ip = "52.3.72.231"
# }

