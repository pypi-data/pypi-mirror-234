import argparse
import json
from typing import Dict, List, Optional


def load_args(argv: List[str], default_args: Optional[Dict] = None):
    conf_parser = argparse.ArgumentParser(description="Configuration file", add_help=False)

    conf_parser.add_argument("-c", "--conf_file", help="Specify config file", metavar="FILE")
    args, remaining_args = conf_parser.parse_known_args(argv)

    defaults = {
        "gateway_address": "https://dask.prod.oceandata.xyz/services/dask-gateway",
        "gateway_proxy_address": "gateway://dask-gw.prod.oceandata.xyz:80",
        "gateway_public_address": "https://dask.prod.oceandata.xyz/services/dask-gateway",
        "gateway_auth": "jupyterhub",
    }

    if default_args:
        defaults.update(default_args)

    if args.conf_file:
        config = json.loads(args.conf_file)
        defaults.update(config)

    parser = argparse.ArgumentParser(parents=[conf_parser])

    parser.add_argument("--gateway-address", help="Dask gateway address")
    parser.add_argument("--gateway-proxy-address", help="Dask gateway proxy address")
    parser.add_argument("--gateway-public-address", help="Dask gateway public address")
    parser.add_argument("--gateway-token", help="Dask gateway API token", default=None)
    parser.add_argument("--cluster-min-workers", default=0)
    parser.add_argument("--cluster-max-workers", default=3)
    parser.add_argument("--az-storage-connstr", help="Azure storage connection string")
    parser.add_argument("--az-storage-container", help="Azure storage container name")
    parser.add_argument("--year", help="Year of the data separated by comma")
    parser.add_argument("--n-workers", help="Number of workers", type=int)
    parser.add_argument("--connection-string", help="connection string to azure blob storage")
    parser.add_argument("--wod-container", help="Name of the container for wod netcdf files")
    parser.add_argument("--target-username", help="DB username")
    parser.add_argument("--target-password", help="DB password")
    parser.add_argument("--target-db-host", help="DB Host")
    parser.add_argument("--target-port", help="DB Port")
    parser.add_argument("--target-db-name", help="DB Name")
    parser.add_argument("--cast-table-name", help="Table Name to write the casts")
    parser.add_argument("--observation-table-name", help="Table Name to write the observations")
    parser.add_argument("--datasets-table-name", help="Table Name to write the OBIS - datasets")
    parser.add_argument("--occurrences-table-name", help="Table Name to write the OBIS - occurrences")
    parser.add_argument("--taxa-table-name", help="Table Name to write the Worms - taxa")
    parser.add_argument(
        "--taxon-rank-table-name",
        help="Table Name to write the Worms - taxon rank table",
    )

    parser.set_defaults(**defaults)

    return parser.parse_args(remaining_args)
