# MODULES
from .. import os, defaultdict, timer

# LIBS
from . import io_lib, py_lib

# MODELS
from ..models.tests import TestGroup, AlphaTest, TestCategories, Levels

# CORE
from core import core

LOG = core.get_logger("tests")

CATEGORIES = {}


def __group_parameters(
    name: str | None = None,
    names: list[str] | None = None,
    group: str | None = None,
    groups: list[str] | None = None,
    category: str | None = None,
    categories: list[str] | None = None,
):
    categories = categories if categories is not None else []
    groups = groups if groups is not None else []
    names = names if names is not None else []

    if category is not None:
        categories.append(category)
    if group is not None:
        groups.append(group)
    if name is not None:
        names.append(name)
    categories = [x.strip() for x in categories]
    groups = [x.strip() for x in groups]
    names = [x.strip() for x in names]
    return categories, groups, names


def process_test_categories(
    categories,
    groups: list[str] = [],
    names: list[str] = [],
    levels: list[Levels] = [],
    run: bool = False,
    coverage: str | None = None,
    load_from_db: bool = True,
    stop: bool = True,
    failed_only: bool = False,
):
    subclasses = AlphaTest.__subclasses__()
    subclasses_by_module = defaultdict(list)
    for subclass in subclasses:
        module_name = subclass.__module__.split(".")[0]
        subclasses_by_module[module_name].append(subclass)

    test_categories = TestCategories()
    for category, class_list in subclasses_by_module.items():
        groups_str = ", ".join([x.__name__ for x in class_list])
        LOG.info(
            f"Loaded test module <{category}> with test groups: {groups_str[:100]} ..."
        )

        for el in class_list:
            test_group = TestGroup(el, coverage=coverage is not None)

            if len(categories) != 0 and test_group.category not in categories:
                continue
            if len(groups) != 0 and test_group.name not in groups:
                continue

            if LOG is not None:
                LOG.debug(f"Found function group <{test_group.name}>")

            test_categories.add_test_group(test_group)

    if load_from_db or failed_only:
        test_categories.get_from_database()
    if run:
        test_categories.test_all(names, levels, stop=stop, failed_only=failed_only)

    return test_categories


def get_tests_auto(
    name: str | None = None,
    names: list[str] | None = None,
    group: str | None = None,
    groups: list[str] | None = None,
    category: str | None = None,
    categories: list[str] | None = None,
    file_path: str | None = None,
    run: bool = False,
    load_from_db: bool = False,
    report: str | None = None,
    coverage: str | None = None,
    levels: list[Levels] | None = None,
    stop: bool = False,
    failed_only: bool = False,
) -> TestCategories:
    """Get the TestCategories class, containings all required tests.

    Args:
        tests_modules (list[str]): list of test modules path
        tests_modules (list[str]): list of test modules path
        name (str, optional): the name of the test to select. Defaults to None.
        group (str, optional): the name of the group to select. Defaults to None.
        category (str, optional): the name of the category to select. Defaults to None.

    Returns:
        TestCategories: [description]
    """
    global CATEGORIES

    categories, groups, names = __group_parameters(
        name, names, group, groups, category, categories
    )

    if run and len(categories) == 0 and len(groups) == 0 and len(names) == 0:
        LOG.info("Requested execution of all tests")
    elif run:
        LOG.info(
            f"Requested execution of tests:\n - categories: {', '.join(categories)}\n - groups: {', '.join(groups)}\n - names: {', '.join(names)}"
        )

    test_categories = process_test_categories(
        categories,
        groups,
        names,
        levels,
        run,
        coverage,
        load_from_db=load_from_db,
        stop=stop,
        failed_only=failed_only,
    )

    if file_path is not None:
        test_categories.to_junit(file_path)

    if report is not None:
        test_categories.report(report)

    if coverage is not None:
        coverages = {}
        for category_name, category in test_categories.categories.items():
            for group_name, group in category.groups.items():
                for test_name, test in group.tests.items():
                    if (
                        test_name in test.coverages
                        and test.coverages[test_name] is not None
                    ):
                        coverages[
                            f"{category_name}-{group_name}-{test_name}"
                        ] = test.coverages[test_name]
        io_lib.archive_object(coverages, coverage)
    return test_categories


def execute_all_tests_auto(directory, output=True, refresh=True, name=None):
    return operate_all_tests_auto(
        directory, output=output, refresh=refresh, name=name, action="execute"
    )


def save_all_tests_auto(directory, output=True, refresh=True, name=None):
    return operate_all_tests_auto(
        directory, output=output, refresh=refresh, name=name, action="save"
    )


def operate_all_tests_auto(
    directory,
    output=True,
    refresh=True,
    name=None,
    action="execute",
    group=None,
    import_path=None,
):
    if refresh:
        py_lib.reload_modules(os.getcwd())

    test_categories = get_tests_auto(group=group, import_path=import_path)

    if action == "execute":
        tests_groups.test_all()
        return tests_groups.print(output=output)
    elif action == "save":
        tests_groups.save_all()
