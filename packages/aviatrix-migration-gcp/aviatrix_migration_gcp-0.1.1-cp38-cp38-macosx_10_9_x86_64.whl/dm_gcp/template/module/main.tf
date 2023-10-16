locals {
  subnet_count    = length(var.avtx_cidrs)
  spoke_gws    = flatten([
    for ac in var.avtx_cidrs: [
      for zone in ac.gw_zones: {
        gw_cidr = ac.cidr
        gw_region_zone = "${var.region}-${zone}"
      }
    ]
  ])
  spoke_gw_count = length(local.spoke_gws)
  avtx_cidrs = [
    for ac in var.avtx_cidrs: ac.cidr
  ]
}

resource "google_compute_subnetwork" "public_gw_subnet" {
  count         = local.subnet_count
  name          = format("%s", "aviatrix-${var.vpc_name}-${var.region}-${count.index+1}")
  ip_cidr_range = var.avtx_cidrs[count.index].cidr
  network       = var.vpc_id
  region        = var.region
}

resource "aviatrix_spoke_gateway" "gw" {
  cloud_type                        = 4
  account_name                      = var.account_name
  gw_name                           = var.spoke_gw_name
  vpc_id                            = var.vpc_name
  vpc_reg                           = local.spoke_gws[0].gw_region_zone
  insane_mode                       = var.hpe
  gw_size                           = var.avtx_gw_size
  subnet                            = local.spoke_gws[0].gw_cidr
  included_advertised_spoke_routes  = var.switch_traffic ? var.vpc_cidrs : join(",", local.avtx_cidrs)
  customized_spoke_vpc_routes       = var.switch_traffic ? var.spoke_routes : var.initial_spoke_routes
  single_az_ha                      = true
{% if data.configure_spoke_gw_hs == "true" %}
  manage_ha_gateway                 = false
  enable_global_vpc                 = true
{% else %}
  ha_gw_size                        = local.spoke_gw_count > 1 ? var.avtx_gw_size : null
  ha_zone                           = local.spoke_gw_count > 1 ? local.spoke_gws[1].gw_region_zone : null
  ha_subnet                         = local.spoke_gw_count > 1 ? local.spoke_gws[1].gw_cidr : null
{% endif %}
  depends_on = [ google_compute_subnetwork.public_gw_subnet ]
}

{% if data.configure_spoke_gw_hs == "true" %}
resource "aviatrix_spoke_ha_gateway" "ha1" {
  count           = local.spoke_gw_count > 1 ? 1 : 0
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${var.spoke_gw_name}-${count.index + 1}"
  subnet          = local.spoke_gws[count.index+1].gw_cidr
  zone            = local.spoke_gws[count.index+1].gw_region_zone
  insane_mode     = var.hpe
  insane_mode_az  = local.spoke_gws[count.index+1].gw_region_zone
  depends_on      = [ google_compute_subnetwork.public_gw_subnet ]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}

resource "aviatrix_spoke_ha_gateway" "ha2" {
  count           = local.spoke_gw_count > 2 ? max(local.spoke_gw_count -2, 0) : 0
  primary_gw_name = aviatrix_spoke_gateway.gw.id
  gw_name         = "${var.spoke_gw_name}-${count.index + 2}"
  subnet          = local.spoke_gws[count.index+2].gw_cidr
  zone            = local.spoke_gws[count.index+2].gw_region_zone
  insane_mode     = var.hpe
  insane_mode_az  = local.spoke_gws[count.index+2].gw_region_zone
  depends_on      = [aviatrix_spoke_ha_gateway.ha1]

  lifecycle {
    ignore_changes = [insane_mode_az]
  }
}
{% endif %}

resource "aviatrix_spoke_transit_attachment" "attachment" {
    spoke_gw_name = aviatrix_spoke_gateway.gw.gw_name
    transit_gw_name = var.transit_gw
{% if data.configure_spoke_gw_hs == "true" %}    
    depends_on = [aviatrix_spoke_ha_gateway.ha1, aviatrix_spoke_ha_gateway.ha2]
{% endif %}    
}

resource "aviatrix_segmentation_network_domain_association" "spoke" {
  count                = var.domain != "" ? 1 : 0
  transit_gateway_name = aviatrix_spoke_transit_attachment.attachment.transit_gw_name
  network_domain_name  = var.domain
  attachment_name      = aviatrix_spoke_gateway.gw.gw_name
}
