import logging

from pingsafe_cli.cli.registry import HttpMethod, GET_CONFIG_DATA_URL, InvalidInput
from pingsafe_cli.cli.utils import make_request, add_global_config_file, add_iac_config_file, \
    add_secret_config_file, add_vulnerability_config_file, upsert_pingsafe_cli
from urllib.parse import urlparse

LOGGER = logging.getLogger("cli")


def set_configs(args):
    parsed_url = urlparse(args.endpoint_url)
    if parsed_url.scheme != "http" and parsed_url.scheme != "https":
        raise InvalidInput("Please add a valid protocol.")
    args.endpoint_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    response = make_request(HttpMethod.GET, args.endpoint_url + GET_CONFIG_DATA_URL, args.api_token)
    admin_configs = response.json()

    add_global_config_file(args, admin_configs)
    add_iac_config_file(args.cache_directory, admin_configs)
    add_secret_config_file(args.cache_directory, admin_configs)
    add_vulnerability_config_file(args.cache_directory, admin_configs)

    upsert_pingsafe_cli(args.cache_directory)
    LOGGER.info("PingSafe CLI Configured Successfully!")
    return 0
