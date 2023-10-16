# -*- coding: utf-8 -*-

# Because external_dependencies is not supported for Odoo version < 7.0
try:
    import coverage
except ImportError:
    raise ImportError("Please install coverage package")

import logging
import os
import subprocess
import sys
import threading
from distutils.version import LooseVersion
from functools import partial

try:
    # For Odoo 16
    from odoo import release
    from odoo.service import common
    from odoo.service.db import check_super
    from odoo.tests.common import HttpCase, BaseCase
    from odoo.tools import config
except ImportError:
    try:
        # For Odoo 10.0
        from odoo import release
        from odoo.service import common
        from odoo.service.db import check_super
        from odoo.tests.common import HttpCase
        from odoo.tools import config
    except ImportError:
        try:
            # For Odoo 9.0
            from openerp import release
            from openerp.service import common
            from openerp.service.db import check_super
            from openerp.tests.common import HttpCase
            from openerp.tools import config
        except ImportError:
            try:
                # For Odoo 8.0
                from openerp import release
                from openerp.service import common
                from openerp.service.security import check_super
                from openerp.tests.common import HttpCase
                from openerp.tools import config
            except ImportError:
                try:
                    # For Odoo 6.1 and 7.0
                    from openerp import release
                    from openerp.service.security import check_super
                    from openerp.service.web_services import common
                    from openerp.tools import config
                except ImportError:
                    try:
                        # For Odoo 5.0 and 6.0
                        import release
                        from service.security import check_super
                        from service.web_services import common
                        from tools import config
                    except ImportError:
                        raise ImportError("Odoo version not supported")

from .. import tools

_logger = logging.getLogger(__name__)

# Because external_dependencies is not supported for Odoo version < 7.0
try:
    import websocket
except ImportError:
    websocket = None
    _logger.warning("Please install websocket-client package")

OMIT_FILES = [
    "__manifest__.py",
    "__openerp__.py",
    "__terp__.py",
    "__init__.py",
]
OMIT_DIRS = ["web", "static", "controllers", "doc", "test", "tests"]


class NewServices:
    @staticmethod
    def _get_coverage_sources():
        coverage_sources = []
        if config.get("code_path"):
            for relpath in config["code_path"].split(","):
                for dirpath, dirnames, filenames in os.walk(relpath):
                    for omit in OMIT_DIRS:
                        if "*/%s/*" % omit in dirpath:
                            break
                    else:
                        for filename in filenames:
                            if (
                                filename.endswith(".py")
                                and filename not in OMIT_FILES
                            ):
                                coverage_sources.append(
                                    os.path.join(dirpath, filename)
                                )
        return coverage_sources

    @staticmethod
    def coverage_start():
        if hasattr(common, "coverage"):
            return False
        _logger.info("Starting code coverage...")
        data_file = config.get("coverage_data_file") or "/tmp/.coverage"
        common.coverage = coverage.coverage(branch=True, data_file=data_file)
        common.coverage.exclude("(.*?)fields.(.*?)")
        common.coverage.start()
        return True

    @staticmethod
    def coverage_stop():
        if not hasattr(common, "coverage"):
            return False
        _logger.info("Stopping code coverage...")
        common.coverage.stop()
        common.coverage.save()
        coverage_result = tools.test_utils._get_coverage_result_file()
        sources = NewServices._get_coverage_sources()
        common.coverage.xml_report(
            morfs=sources,
            outfile=coverage_result,
            ignore_errors=True,
        )
        del common.coverage
        return True

    @staticmethod
    def run_tests(dbname, modules=None, with_coverage=True):
        init_test_enable = config.get("test_enable")
        config["test_enable"] = True
        threading.currentThread().dbname = dbname
        modules = tools.filter_modules_list(dbname, modules)
        tools.test_utils._remove_results_files()
        tools.run_unit_tests(dbname, modules)
        tools.run_other_tests(dbname, modules)
        config["test_enable"] = init_test_enable
        return True

    @staticmethod
    def prepare_results_files():
        result = {"tests": {}}
        coverage_result_file = tools.test_utils._get_coverage_result_file()
        test_result_directory = tools.test_utils._get_test_result_directory()
        for file in os.listdir(test_result_directory):
            file_path = os.path.join(test_result_directory, file)
            with open(file_path, "r") as test:
                result["tests"][file] = test.read()
        with open(coverage_result_file, "r") as file:
            result["coverage"] = file.read()
        return result


native_dispatch = common.dispatch
additional_methods = [
    attr
    for attr in dir(NewServices)
    if not attr.startswith("_") and callable(getattr(NewServices, attr))
]

# TODO: Fix error
""" if websocket is not None and 'HttpCase' in dir():
    # Launch HttpCase to execute tests concerning controllers
    try:
        HttpCase().start_browser()
    except TypeError:
        try:
            HttpCase().start_browser(_logger)
        except TypeError:
            _logger.error('Chrome not initialized')
    else:
        _logger.info('Chrome initialized') """


def new_dispatch(*args):
    i = LooseVersion(release.major_version) < LooseVersion("8.0") and 1 or 0
    method = args[i]
    if method in additional_methods:
        params = args[i + 1]
        admin_passwd, params = params[0], params[1:]
        check_super(admin_passwd)
        return getattr(NewServices, method)(*params)
    return native_dispatch(*args)


common.dispatch = new_dispatch


@classmethod
def tearDownClass(cls):
    if hasattr(cls, "cr"):
        cls.cr.close()
    old_tearDownClass()


old_tearDownClass = BaseCase.tearDownClass
BaseCase.tearDownClass = tearDownClass
