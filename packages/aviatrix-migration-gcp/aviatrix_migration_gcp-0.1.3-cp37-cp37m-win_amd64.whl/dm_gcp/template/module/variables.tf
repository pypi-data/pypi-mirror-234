variable "var_project" {
  default = "aviatrix-gcp-19850"
}
variable "vpc_name" {}
variable "vpc_id" {}
variable "region" {}
variable "avtx_cidrs" {
  type = list(any)
}

variable "account_name" {}
variable "spoke_gw_name" {}
variable "transit_gw" {}
variable "avtx_gw_size" {}
variable "hpe" {
  default = false
}
variable "domain" {
  description = "Provide security domain name to which spoke needs to be deployed. Transit gateway mus tbe attached and have segmentation enabled."
  type        = string
  default     = ""
}
variable "spoke_routes" {
  description = "A list of comma separated CIDRs to be customized for the spoke VPC routes. When configured, it will replace all learned routes in VPC routing tables, including RFC1918 and non-RFC1918 CIDRs. It applies to this spoke gateway only"
  type        = string
  default     = null
}
variable "initial_spoke_routes" {
  description = "A list of comma separated CIDRs to be customized for the spoke VPC routes at staging time."
  type        = string
  default     = ""
}
variable "switch_traffic" {}
variable "vpc_cidrs" {
  description = "A list of comma separated CIDRs to be advertised to on-prem as Included CIDR List. When configured, it will replace the default advertised routes of subnets within the region."
  type        = string
  default     = null
}
