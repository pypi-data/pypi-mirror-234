provider "google" {
  project     = var.project_id
{% if data.gcp_cred is not none %}
  credentials = file("{{data.gcp_cred}}")
{% endif %}
}

provider "aviatrix" {
  controller_ip = var.controller_ip
}