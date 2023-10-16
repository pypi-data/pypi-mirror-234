# -*- coding: utf-8 -*-
"""Configuration options for Azure discovery migration."""
import ipaddress
import json
import pathlib
import typing as t

import yaml
import pydantic
from pydantic import constr  # Constrained string type.
from pydantic import Field, ValidationError, root_validator, validator

from dm_gcp.res.AviatrixProviderVersion import AviatrixProviderVersion
from dm_gcp.res.Globals import Globals

if not hasattr(t, "Literal"):
    from typing_extensions import Literal

    t.Literal = Literal


AzureRegionName = t.Literal[
    "westus",
    "eastus",
    "centralus",
    "westus2",
    "northeurope",
    "westeurope",
    "southeastasia",
    "japaneast",
    "chinaeast2",
    "chinanorth2",
]
CleanupResources = t.Literal[
    "PEERING",
    "VNG_ER",
]

CIDRList = t.List[ipaddress.IPv4Network]
Tag = t.Dict[str, str]
Tags = t.List[Tag]
_str = constr(strip_whitespace=True)


def _default_network() -> CIDRList:
    return [ipaddress.IPv4Network("0.0.0.0/0")]

class _BaseModel(pydantic.BaseModel):
    discovery_only: t.ClassVar[bool] = False

    class Config:
        json_encoders = {
            ipaddress.IPv4Address: str,
            ipaddress.IPv4Network: str,
        }
        extra = "forbid"


class BackupConfig(_BaseModel):
    """Backup account folder.

    Uses cloud storage to backup the generated account folder.
    Omit this section if backup is not required.

    Note:
        Currently only S3 backup is supported.

    Attributes:
        s3: S3 backup configuration.
    """

    class S3Config(_BaseModel):
        """Setup S3 for storing the terraform output files.

        Attributes:
            account: S3 bucket account number.
            role_name: S3 bucket access permission.
            name: S3 bucket name.
            region: S3 bucket region.
        """

        account: _str
        role_name: _str
        name: _str
        region: _str

    s3: S3Config


class TfControllerAccessConfig(_BaseModel):
    """
    Attributes:
        mode: if "ENV" is used, AVIATRIX_USERNAME and AVIATRIX_PASSWORD should be set for terraform use.
    """

    alias: _str = "us_west_2"
    mode: t.Literal["ENV", "SSM"] = "ENV"
    region: _str = "us-west-2"
    password_store: _str = "avx-admin-password"
    ssm_role: _str = ""
    username: _str = "admin"
    account_id: constr(strip_whitespace=True, regex=r"^[0-9]*$") = ""

    @root_validator(pre=True)
    def check_mode(cls, values):
        """
        Avoid confusion, do not allow other attributes if ENV is used.
        """

        if cls.discovery_only:
            return values

        if "mode" in values and values["mode"] == "ENV":
            if len(values) > 1:
                lvalues = dict(values)
                del lvalues["mode"]
                raise ValueError(
                    f"When aviatrix.tf_controller_access.mode is 'ENV', "
                    f"the following attribute(s) {lvalues} should be removed."
                )

        # if ssm_role is defined, account_id is mandatory
        if "mode" in values and values["mode"] == "SSM":
            if (
                "ssm_role" in values
                and len(values["ssm_role"]) > 0
                and (not "account_id" in values or not len(values["account_id"]) > 0)
            ):
                raise ValueError(f"missing account_id")
        return values


class TfCloudConfig(_BaseModel):
    organization: t.Optional[_str] = None
    workspace_name: t.Optional[_str] = None
    tags: t.Optional[t.List[_str]] = None

    @root_validator(pre=True)
    def check_required_attributes(cls, values):
        """
        check required attributes are there:
        - organization attribute is mandatory;
        - only one of workspace_name and tags attributes is allowed and required.
        check if
        """
        if cls.discovery_only:
            return values

        if "organization" not in values or not values["organization"]:
            raise ValueError("Missing organization name")
        if "workspace_name" not in values and "tags" not in values:
            raise ValueError(
                "Required workspace_name or tags atttribute to be defined"
            )
        if "workspace_name" in values and "tags" in values:
            raise ValueError("Either workspace_name or tags is allowed")
        return values

    @validator("workspace_name")
    def check_not_empty(cls, val):
        if cls.discovery_only:
            return val

        if not val:
            raise ValueError("Missing workspace_name")
        return val

    @validator("tags")
    def check_and_rewrite_tags(cls, v):
        """
        1. If tags list is empty, raise error
        2. Convert input tags (list of string), e.g., ['abc', 'dec'] into
           a string tags with double quote, e.g., '["abc", "dec"]'.
           This will facilitate terraform tags generation, which requires a list
           of double quote string.

           Performing the conversion here seems to be pretty clean; otherwise,
           it can be done inside common.readGlobalConfigOption.

           *** Of course, we are changing the tags type in such conversion,
           *** seems to be allowed by pydantic.
        """
        if v == None:
            raise ValueError("Empty tag not allowed")

        if len(v) == 0:
            raise ValueError("tags list cannot be empty")

        if not all([x for x in v]):
            raise ValueError("Empty tag not allowed")

        return json.dumps(v)


class TerraformConfig(_BaseModel):
    """Terraform configuration.

    Attributes:
        terraform_output: Absolute path to the TF files created.
        terraform_version: Terraform version in terraform version syntax
        aviatrix_provider: Aviatrix terraform provider version in
            terraform version syntax
        aws_provider: AWS terraform provider version in terraform version syntax
        enable_s3_backend: Generate terraform S3 backend config.
            Default to True.
        module_source:  Override the module source in `vpc.tf`. If this is
            omitted or "", we use the included TF module source.
            Defaults to "".
    """

    DEFAULT_MODULE_SOURCE: t.ClassVar[_str] = "../module_gcp_brownfield_spoke_vpc"
    DEFAULT_MODULE_NAME: t.ClassVar[_str] = "module_gcp_brownfield_spoke_vpc"

    regenerate_common_tf: bool = True
    account_folder: t.Literal["name", "id"] = "id"
    terraform_output: _str
    terraform_version: _str  # = ">= 0.14"
    aviatrix_provider: _str  # "= 2.19.3"
    # aws_provider: _str  # "~> 3.43.0"
    # arm_provider: _str  # "~> 2.89.0"
    enable_s3_backend: bool = False
    module_source: t.Optional[_str] = DEFAULT_MODULE_SOURCE
    module_name: t.Optional[_str] = DEFAULT_MODULE_NAME
    tf_cloud: t.Optional[TfCloudConfig] = None
    tmp_folder_id: t.Optional[_str] = None

    @validator("aviatrix_provider")
    def validateAviatrixProviderVersion(cls, val):
        Globals.setAvxProvider(val)
        return val
    
    @validator("tf_cloud")
    def check_tfcloud_for_none(cls, val, values):
        """
        handle tfcloud None case where none of its attributes are defined.
        """
        if cls.discovery_only:
            return val

        if val is None:
            raise ValueError("missing organization, workspace_name, tags attributes")
        return val

    @validator("tmp_folder_id")
    def validate_tmp_folder_id(cls, val):

        if val is not None and val != "VPC_ID" and val != "YAML_ID":
            raise ValueError('Valid input for tmp_folder_id is "VPC_ID" or "YAML_ID"')
        
        return val





class AviatrixConfig(_BaseModel):
    """Aviatrix config for onboarding.

    Attributes:
        controller_ip: Aviatrix controller IP address.
        tf_controller_access: terraform attributes for accessing controller password, via AWS SSM or ENV
    """

    controller_ip: ipaddress.IPv4Address
    tf_controller_access: TfControllerAccessConfig = Field(
        default_factory=TfControllerAccessConfig
    )


class AlertConfig(_BaseModel):
    """Alert configuration."""

    vpc_name_length: int = 31
    vnet_peering: bool = True
    vcpu_limit: bool = True  # Requires Microsoft.Capacity registration, see README
    check_gateway_existence: t.Optional[bool] = True


class ScriptConfig(_BaseModel):
    """Configuration for script features.

    Attributes:
        allow_vnet_cidrs: List of allowed VPC CIDRs. Only the allowed CIDRs will
            be copied to vpc_cidr and passed to the brownfield spoke VPC
            terraform module. Set it to [“0.0.0.0/0”] to allow any CIDR.
        configure_gw_name:
        configure_spoke_advertisement:
        enable_spoke_egress:
        route_table_tags: List of tags to be added to the route table(s). Omit
            this section if no tags required.
            Defaults to [].
        subnet_tags: List of tags to be added to the subnet(s). Omit this
            section if no tags required.
            Defaults to [].
    """

    allow_vnet_cidrs: CIDRList = Field(default_factory=_default_network)
    # configure_gw_name: bool = True
    configure_spoke_advertisement: bool = False
    configure_spoke_gw_hs: t.Optional[bool] = False
    route_table_tags: Tags = Field(default_factory=list)
    enable_spoke_split_cidr: t.Optional[bool] = False
    configure_private_subnet: t.Optional[bool] = False
    # subnet_tags: Tags = Field(default_factory=list)


# class TGWConfig(_BaseModel):
#     """Transit gateways.
#
#     Attributes:
#         tgw_account: TGW account number.
#         tgw_role: TGW account access role.
#         tgw_by_region: Dictionary of TGW Regions to TGW ID.
#             e.g.: {"us-east-1": "tgw-020a8339660950770"}
#     """
#
#     tgw_account: _str
#     tgw_role: _str
#     tgw_by_region: t.Dict[AzureRegionName, _str] = Field(default_factory=dict)


GWName = constr(strip_whitespace=True, max_length=50)


class VWanConfig(_BaseModel):
    project_id: _str
    resource_group: _str
    vhub: _str


class AvtxCidrConfig(_BaseModel):
    cidr: _str
    gw_zones: t.List[_str]


class CloudRouterConfig(_BaseModel):
    router_name: _str
    region: _str
    remove_advertised_routes: t.List[t.Union[ipaddress.IPv4Network,ipaddress.IPv4Address]] = []
    remove_advertised_groups: t.List[_str] = []
    add_advertised_routes: t.List[t.Union[ipaddress.IPv4Network,ipaddress.IPv4Address]] = []
    add_advertised_groups: t.List[_str] = []


class TransitVpcConfig(_BaseModel):
    vpc_name: _str
    cloud_routers: t.List[CloudRouterConfig] = []


class RegionConfig(_BaseModel):    
    """Settings for VPC migration.

    Attributes:
    """
    region: _str
    avtx_cidr: t.Optional[_str] = None
    avtx_cidrs: t.List[AvtxCidrConfig]
    domain: t.Optional[_str] = None
    inspection: t.Optional[bool] = None
    spoke_advertisement: t.Optional[t.List[_str]] = None
    initial_spoke_routes: t.Optional[CIDRList] = ["1.1.1.1/32"]
    spoke_routes: t.Optional[CIDRList] = None
    spoke_gw_name: t.Optional[GWName] = None
    transit_gw_name: t.Optional[GWName] = None
    spoke_gw_tags: Tags = Field(default_factory=list)
    spoke_gw_size: t.Optional[_str] = None
    hpe: t.Optional[bool] = None
    max_hpe_performance: t.Optional[bool] = None
    advertise_gke: t.Optional[bool] = False


    @validator("max_hpe_performance")
    def validate_max_hpe_performance(cls, val, values):
        if cls.discovery_only:
            return val

        avxProviderVersionStr = Globals.getAvxProvider()
        avxProvider = AviatrixProviderVersion(avxProviderVersionStr)
        if avxProvider.lessThan("2.22.3"):
            raise ValueError('attribute max_hpe_performance is available only if aviatrix_provider is >= 2.22.3')

        hpe = values.get("hpe", None)
        if hpe is not None and hpe == False and val is not None:
            raise ValueError('attribute max_hpe_performance is available only if hpe is set to True')
        return val


class VpcConfig(_BaseModel):
    vpc_name: _str
    regions: t.List[RegionConfig]
    transit_vpcs: t.List[TransitVpcConfig] = []


class AccountInfo(_BaseModel):
    """Information about spoke VPCs.

    Attributes:
        project_id: Azure Subscription ID.
        account_name: Name of the VNet account owner.
        hpe: Enable high performance encryption on spoke gateways.
            Defaults to True.
        filter_cidrs: Filters out any route within specified CIDR when copying
            the route table. No need to add RFC1918 routes in the list; they
            are filtered by default. Set it to empty list [] if no filtering required.
        spoke_gw_size: Spoke gateway instance size.
        add_account:
        onboard_account:
        vpcs:
    """

    project_id: _str
    account_name: _str
    vpcs: t.List[VpcConfig]
    tf_provider_alias: t.Optional[_str] = None
    hpe: bool = True
    filter_cidrs: CIDRList = Field(default_factory=list)
    spoke_gw_size: _str = "n1-standard-1"
    onboard_account: bool = False
    max_hpe_performance: t.Optional[bool] = None

    @validator("max_hpe_performance")
    def validate_max_hpe_performance(cls, val, values):
        if cls.discovery_only:
            return val

        avxProviderVersionStr = Globals.getAvxProvider()
        avxProvider = AviatrixProviderVersion(avxProviderVersionStr)
        if avxProvider.lessThan("2.22.3"):
            raise ValueError('attribute max_hpe_performance is available only if aviatrix_provider is >= 2.22.3')

        hpe = values.get("hpe", None)
        if hpe is not None and hpe == False and val is not None:
            raise ValueError('attribute max_hpe_performance is available only if hpe is set to True')
        return val


class PrestageConfig(_BaseModel):
    """Settings used during prestage."""

    default_route_table: _str = "dummy_rt"


class SwitchTrafficConfig(_BaseModel):
    """Settings used during `switch_traffic.

    Attributes:
        transit_peerings: Dictionary of azure transit peered to aws transit
             e.g.: {"azure-transit-useast-1": "aws-transit-us-east-1"}
        default_route_table: _str
        delete_vnet_lock: bool
    """

    transit_peerings: t.Dict[_str, _str] = Field(default_factory=dict)
    delete_vnet_lock: bool = True


class CleanupConfig(_BaseModel):
    """Resources to cleanup.

    Attributes:
        delete_vnet_lock:
        resources: Delete resources like `VGW` or `VIF` in a VPC.
    """

    delete_vnet_lock: bool = True
    resources: t.List[CleanupResources] = Field(default_factory=list)


GW_NAME_KEYS = ["spoke_gw_name", "transit_gw_name"]


class CloudRouterConfig(_BaseModel):
    router_name: _str
    region: _str
    remove_advertised_routes: t.List[t.Union[ipaddress.IPv4Network,ipaddress.IPv4Address]] = []
    remove_advertised_groups: t.List[_str] = []


class TransitVpcConfig(_BaseModel):
    vpc_name: _str
    cloud_routers: t.List[CloudRouterConfig] = []


class DiscoveryConfiguration(_BaseModel):
    """Discovery Migration Configuration.

    Attributes:
        aviatrix: Generate terraform resource for onboarding an Aviatrix account.
        alert: Alerts configuration.
        config: Script feature configuration.
        tgw: List of TGWs used, assuming all TGWs are defining within one account.
        account_info: Spoke VPC info.
        switch_traffic: Configuration during switch_traffic.
        cleanup: Resources to cleanup.
        aws: Use AWS S3 to backup the generated account folder.
        terraform: Mark the beginning of terraform info.
    """

    label: t.Literal["GCP"]
    terraform: TerraformConfig
    aviatrix: AviatrixConfig
    gcp_cred: t.Optional[_str] = None
    account_info: t.List[AccountInfo]
    alert: AlertConfig = Field(default_factory=AlertConfig)
    cleanup: CleanupConfig = Field(default_factory=CleanupConfig)
    config: ScriptConfig = Field(default_factory=ScriptConfig)
    prestage: PrestageConfig = Field(default_factory=PrestageConfig)
    switch_traffic: SwitchTrafficConfig = Field(default_factory=SwitchTrafficConfig)
    aws: t.Optional[BackupConfig] = None
    # tgw: t.Optional[TGWConfig] = None

    @validator("config")
    def check_config(cls, val, values):
        """
        Validate gateway names.
        Validate number of regions when configure_spoke_gw_hs is False.

        Args:
            val: The account_info dictionary.
            values: All values passed to DiscoveryConfiguration init.

        returns:
            The account_info dictionary.
        """
        if cls.discovery_only:
            return val

        config = val
        errors = []
        account_info = values.get("account_info", [])

        for account in account_info:
            for vpc in account.vpcs:
                for region in vpc.regions:
                    if any(getattr(region, key) is None for key in GW_NAME_KEYS):
                        errors.append((account.project_id, vpc.vpc_name, region.region))
        if errors:
            error_vpc_str = "\n".join(
                f"account: {account_id}, vpc: {vpc_name}, region: {region}"
                for account_id, vpc_name, region in errors
            )
            raise ValueError(
                "'both 'spoke_gw_name' and"
                " 'transit_gw_name' must be set in all VPCs."
                "\nList of nonconforming VPCs:\n"
                f"{error_vpc_str}"
            )

        # for classic spoke, if number of regions > 1, raise error
        if config.configure_spoke_gw_hs == False:
            for account in account_info:
                for vpc in account.vpcs:
                    if len(vpc.regions) > 1:
                        errors.append((account.project_id, vpc.vpc_name))
        if errors:
            error_vpc_str = "\n".join(
                f"account: {account_id}, vpc: {vpc_name}"
                for account_id, vpc_name in errors
            )
            raise ValueError(
                "'config.configure_spoke_gw_hs' is False, spoke gateway(s) only allowed in one region"
                "\nList of nonconforming VPCs:\n"
                f"{error_vpc_str}"
            )
        
        # for classic spoke, if total number of gw_zone > 2, raise error
        if config.configure_spoke_gw_hs == False:
            for account in account_info:
                for vpc in account.vpcs:
                    if len(vpc.regions) == 1:
                        num_zones = 0
                        for avtx_cidr in vpc.regions[0].avtx_cidrs:
                            num_zones = num_zones + len(avtx_cidr.gw_zones)
                        if num_zones > 2:
                            errors.append((account.project_id, vpc.vpc_name, vpc.regions[0].region))
        if errors:
            error_vpc_str = "\n".join(
                f"account: {account_id}, vpc: {vpc_name}, region: {region}"
                for account_id, vpc_name, region in errors
            )
            raise ValueError(
                "'config.configure_spoke_gw_hs' is False, a max of 2 spoke gateway(s) is allowed,"
                f" total gw_zones per VPC cannot exceed 2"
                "\nList of nonconforming VPCs:\n"
                f"{error_vpc_str}"
            )
        return config


def load_from_dict(config_dict: t.Dict, discovery_only: bool = False) -> DiscoveryConfiguration:
    """Load discovery migration settings from a python dictionary.

    Args:
        config_dict: Python dictionary in which to load configuration
            settings from.

    Returns:
        Parsed discovery migration settings.
    """
    _BaseModel.discovery_only = discovery_only

    try:
        config = DiscoveryConfiguration(**config_dict)
    except ValidationError as e:
        print(e.json())
        raise SystemExit(1) from e
    return config


def dump_to_dict(config: DiscoveryConfiguration) -> t.Dict:
    """Dump discovery migration settings to a python dictionary.

    Args:
        config: Discovery migration settings.

    Returns:
        Configuration dictionary.
    """
    json_data = config.json()
    data = json.loads(json_data)

    return data


def load_from_yaml(yml_path: pathlib.Path, discovery_only: bool = False) -> DiscoveryConfiguration:
    """Load discovery migration settings from a yaml.

    Args:
        yml_path: Path to location of discovery migration yaml.

    Returns:
        Parsed discovery migration settings.
    """
    with open(yml_path, "r") as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)

    return load_from_dict(data, discovery_only=discovery_only)


def dump_to_yaml(config: DiscoveryConfiguration, dest: pathlib.Path) -> pathlib.Path:
    """Dump discovery migration settings to a yaml file.

    Args:
        config: Discovery migration settings.
        dest: Path to destination location of discovery migration yaml.

    Returns:
        Path to destination location of discovery migration yaml.
    """
