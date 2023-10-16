variable "{{data.var_avtx_cidrs}}" {}

module "{{ data.vpc_name }}-{{data.region}}" {
  source                 = "{{data.module_source}}"
  account_name           = "{{data.account_name}}"
  vpc_name               = "{{data.vpc_name}}"
{% if data.var_vpc_cidrs is not none %}
  vpc_cidrs              = "{{data.var_vpc_cidrs}}"
{% endif %}
  vpc_id                 = "projects/${var.project_id}/global/networks/{{ data.vpc_name }}"
  region                 = "{{data.region}}"
  avtx_cidrs             = var.{{data.var_avtx_cidrs}}
  spoke_gw_name          = "{{data.spoke_gw_name}}"
  transit_gw             = "{{data.transit_gw_name}}"
  avtx_gw_size           = "{{data.spoke_gw_size}}"
  hpe                    = {{data.hpe}}
{% if data.domain is not none %}
  domain                 = "{{data.domain}}"
{% endif %}
{% if data.var_spoke_routes is not none %}
  spoke_routes           = "{{data.var_spoke_routes}}"
{% endif %}
{% if data.var_initial_spoke_routes is not none %}
  initial_spoke_routes   = "{{data.var_initial_spoke_routes}}"
{% endif %}
  switch_traffic         = false
}