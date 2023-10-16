import subprocess, os, psutil, logging, ujson, argparse, time, re, sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Init database")

    parser.add_argument("--project", "-p", help="Project path")
    parser.add_argument("--configuration", "-c", help="Configuration to run")

    parser.add_argument(
        "--tables", "-T", nargs="+", default=None, help="Tables to init"
    )
    parser.add_argument("--binds", "-B", nargs="+", default=None, help="Binds to init")

    parser.add_argument(
        "--create", "-cr", action="store_true", help="Create the tables"
    )
    parser.add_argument("--drop", "-d", action="store_true", help="Drop the tables")
    parser.add_argument(
        "--truncate", "-t", action="store_true", help="Truncate the tables"
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="Force non local configuration"
    )
    parser.add_argument("--init", "-i", action="store_true", help="Init the tables")
    parser.add_argument(
        "--init_views", "-iv", action="store_true", help="Init the tables views"
    )

    args = parser.parse_args()

    if args.project:
        os.chdir(args.project)
        sys.path.append(args.project)

    if args.configuration is not None:
        os.environ["ALPHA_CONF"] = args.configuration

    from core import core

    from ..libs import database_lib

    test_categories = database_lib.init_databases(
        core=core,
        tables=args.tables,
        binds=args.binds,
        create=args.create,
        drop=args.drop,
        truncate=args.truncate,
        force=args.force,
        init=args.init,
        init_views=args.init_views,
    )
