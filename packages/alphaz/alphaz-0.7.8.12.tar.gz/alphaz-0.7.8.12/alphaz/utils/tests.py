import subprocess, os, psutil, logging, ujson, argparse, time, re, sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute test")

    parser.add_argument("--project", "-p", help="Project path")
    parser.add_argument("--configuration", "-c", help="Configuration to run")

    parser.add_argument(
        "--categories", "-CAT", nargs="+", default=[], help="Test categories"
    )
    parser.add_argument("--groups", "-G", nargs="+", default=[], help="Test groups")
    parser.add_argument("--names", "-N", nargs="+", default=[], help="Test names")
    parser.add_argument("--levels", "-L", nargs="+", default=[], help="Test levels")

    parser.add_argument("--run", "-r", action="store_true", help="Run the test or not")
    parser.add_argument(
        "--failed_only", "-fo", action="store_true", help="Run only failed tests"
    )
    parser.add_argument(
        "--database", "-db", action="store_true", help="Load test results from db"
    )
    parser.add_argument("--report", "-re", help="Generate a test report")
    parser.add_argument("--stop", "-s", action="store_true", help="Stop on fail")

    parser.add_argument("--directory", "-d", help="Working directory")
    parser.add_argument("--coverage", "-co", help="Coverage file")

    parser.add_argument("--file", "-fi", help="Output file name")

    parser.add_argument("--binds", "-B", nargs="+", default=[], help="Test levels")
    parser.add_argument("--tables", "-T", nargs="+", default=[], help="Test levels")
    parser.add_argument(
        "--drop", "-dr", action="store_true", help="Run the test or not"
    )
    parser.add_argument(
        "--truncate", "-t", action="store_true", help="Run the test or not"
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="Run the test or not"
    )
    parser.add_argument(
        "--create", "-cr", action="store_true", help="Run the test or not"
    )
    parser.add_argument("--init", "-i", action="store_true", help="Run the test or not")
    parser.add_argument(
        "--init_views", "-iv", action="store_true", help="Run the test or not"
    )

    args = parser.parse_args()

    if args.project:
        os.chdir(args.project)
        sys.path.append(args.project)

    if args.configuration is not None:
        os.environ["ALPHA_CONF"] = args.configuration

    from core import core
    from ..libs import test_lib, database_lib

    if any(
        [
            args.binds,
            args.tables,
            args.drop,
            args.truncate,
            args.force,
            args.create,
            args.init,
            args.init_views,
        ]
    ):
        database_lib.init_databases(
            core,
            binds=args.binds,
            tables=args.tables,
            drop=args.drop,
            truncate=args.truncate,
            force=args.force,
            create=args.create,
            init=args.init,
            init_views=args.init_views,
        )

    test_categories = test_lib.get_tests_auto(
        names=args.names,
        categories=args.categories,
        groups=args.groups,
        file_path=args.file,
        run=args.run,
        coverage=args.coverage,
        load_from_db=args.database,
        report=args.report,
        levels=args.levels,
        stop=args.stop,
        failed_only=args.failed_only,
    )
    sys.exit(0 if test_categories.status else 1)
