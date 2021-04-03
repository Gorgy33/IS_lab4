import json
import sys

from backend.src.application import start_application

import argparse
from backend.src.utils import EnvDefault


def main():

    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        with open(sys.argv[2]) as file:
            start_application(json.load(file))
        exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("--server_host", action=EnvDefault, envvar="SERVER_HOST")
    parser.add_argument("--server_port", action=EnvDefault, envvar="SERVER_PORT", type=int)
    parser.add_argument("--db_user", action=EnvDefault, envvar="DB_USER")
    parser.add_argument("--db_password", action=EnvDefault, envvar="DB_PASSWORD")
    parser.add_argument("--db_host", action=EnvDefault, envvar="DB_HOST")
    parser.add_argument("--db_port", action=EnvDefault, envvar="DB_PORT", type=int)
    parser.add_argument("--db_name", action=EnvDefault, envvar="DB_NAME")
    parser.add_argument("--path_to_template", action=EnvDefault, envvar="PATH_TO_TEMPLATE")
    parser.add_argument("--path_to_static", action=EnvDefault, envvar="PATH_TO_STATIC")
    args = parser.parse_args()

    config = {
        "db_connection_string":
            f"postgres://{args.db_user}:{args.db_password}@{args.db_host}:{args.db_port}/{args.db_name}",
        "host": args.server_host,
        "port": args.server_port,
        "path_to_template": args.path_to_template,
        "path_to_static": args.path_to_static,
    }

    start_application(config)


if __name__ == '__main__':
    main()
