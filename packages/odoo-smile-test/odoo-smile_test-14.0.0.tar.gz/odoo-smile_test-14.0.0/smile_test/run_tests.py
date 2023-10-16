#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from functools import partial
import os, sys
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    import xmlrpc.client as Client
except ImportError:
    import xmlrpclib as Client

def get_options():
    """
    Get options from command line
    :return: Options
    """
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument("-H", "--host", default="http://localhost:8069")
    parser.add_argument(
        "-P", "--password", default="superadmin", help="SuperAdmin password"
    )
    parser.add_argument("-d", "--database")
    parser.add_argument("-u", "--user", default="admin")
    parser.add_argument("-p", "--user_password", default="admin")
    parser.add_argument("-m", "--modules", default='',
                        help="Modules to test (comma separated names)")
    parser.add_argument(
        '-upd', '--update',
        default='',
        help='Update modules before running tests (comma separated names)'
    )
    parser.add_argument("-x", "--xmlrpc", default="xmlrpc/2")
    parser.add_argument('-dest', '--destination', default='tests')
    parser.add_argument('-c', '--coverage', action='store_true', default=True)
    parser.add_argument('-f', '--allow-failures', action='store_true',
                        default=False)
    return parser.parse_args()


class RunTests:
    """
    Class to connect to Odoo server and run tests
    """
    def __init__(self, host, admin_pwd, xmlrpc="xmlrpc/2"):
        """
        :param host: Host of the server
        :param admin_pwd: Password of the admin user
        :param xmlrpc: Xmlrpc version

        :type host: str
        :type admin_pwd: str
        :type xmlrpc: str
        """
        assert xmlrpc in ["xmlrpc/2", "xmlrpc/2/common", "xmlrpc/2/object",
                        "xmlrpc/2/db"]
        self.host = host
        self.xmlrpc = xmlrpc
        self.admin_pwd = admin_pwd
        self.coverage = False

        self.result_coverage = None
        self.total_coverage = 0.0
        self.result_tests = {
            # file_name: xml_content
        }

        # set values by connect method
        self.uid = None
        self.database = None
        self.user = None

    def get_service(self, service):
        """
        Get service from host
        :param service: Service to connect to
        :type service: str

        :return: Service
        """
        assert service in ["common", "object", "db"]
        return Client.ServerProxy(f"{self.host}/{self.xmlrpc}/{service}")

    def connect(self, user, user_pwd, database=None):
        """
        Connect to Odoo server

        :param user: User to connect with
        :param user_pwd: User password
        :param database: Database to connect to

        :type user: str
        :type user_pwd: str
        :type database: str
        """
        if not database:
            database = self.get_service('db').list()[0]

        common = self.get_service('common')
        uid = common.authenticate(database, user, user_pwd, {})
        self.uid = uid
        self.user = user
        self.database = database

    def update_modules(self, modules_list: list):
        """
        Update modules

        :param modules_list: Modules to update
        :type modules_list: list
        """
        if not self.database or not self.uid or not self.user:
            raise ConnectionError(
                "You must connect to the server before updating modules"
            )

        sock_exec = partial(
            self.get_service(
                "object").execute, self.database, self.uid, self.user
        )
        sock_exec("ir.module.module", "update_list")
        module_ids_to_install = []
        for module_name in modules_list:
            module_ids = sock_exec(
                "ir.module.module",
                "search",
                [("name", "=", module_name)],
                0,
                1,
            )
            if module_ids:
                module_ids_to_install.append(module_ids[0])
        try:
            sock_exec(
                "ir.module.module", "button_immediate_upgrade",
                module_ids_to_install
            )
        except Client.Fault as fault:
            msg = fault.faultString
            if msg == "None":
                msg = "Check external dependencies"
            raise f"Error while modules installation\n\n{msg}"

    def run_tests(self, modules_list: list):
        """
        Run tests

        :param modules_list: Modules to test
        :type modules_list: list
        """
        common = self.get_service('common')
        if self.coverage:
            common.coverage_start(self.admin_pwd)
        common.run_tests(self.admin_pwd, self.database, modules_list, True)
        if self.coverage:
            common.coverage_stop(self.admin_pwd)
        res = common.prepare_results_files(self.admin_pwd)
        if res.get('coverage'):
            self.result_coverage = res['coverage']
            self.total_coverage = (
                float(
                    ET.fromstring(res['coverage']).attrib["line-rate"]
                    ) * 100
            )
        if res.get('tests'):
            self.result_tests = res['tests']

    def get_test_results(self):
        """
        Get tests results by OK, KO
        Return a tuple of two dict:
        - first dict contains OK tests
        - second dict contains KO tests
        """
        if not self.result_tests:
            raise ValueError("You must run tests before getting results")
        failed_tests = {}
        success_tests = {}
        for file_name, test_vals in self.result_tests.items():
            root = ET.fromstring(test_vals)
            if int(root.get("errors", '0')) or int(root.get("failures", '0')):
                failed_tests[file_name] = test_vals
            else:
                success_tests[file_name] = test_vals
        return success_tests, failed_tests

    def save_reports_to_files(self, path):
        """
        :param path: Path to save files
        :type path: str

        Save tests results to files
        return list of file paths
        """
        os.makedirs(path, exist_ok=True)
        file_paths = []
        for file_name in self.result_tests.keys():
            file_path = os.path.join(path, file_name)
            with open(file_path, "w+", encoding='utf-8') as _test_file:
                _test_file.write(self.result_tests.get(file_name, ""))
            file_paths.append(file_path)

        if self.result_coverage:
            coverage_dest = os.path.join(path, "coverage.xml")
            with open(coverage_dest, "w+", encoding='utf-8') as _coverage_file:
                _coverage_file.write(self.result_coverage)
            file_paths.append(coverage_dest)

        return file_paths

if __name__ == "__main__":
    options = get_options()
    RET_CODE = 0
    cnx = RunTests(options.host, options.password, options.xmlrpc)
    cnx.coverage = options.coverage
    cnx.connect(options.user, options.user_password, options.database)
    if options.update:
        update_modules = options.update.split(",") if options.update else []
        cnx.update_modules(update_modules)

    modules = options.modules.split(",") if options.modules else []
    cnx.run_tests(modules)

    test_result_directory = options.destination
    if test_result_directory:
        cnx.save_reports_to_files(test_result_directory)

    success_tests, failed_tests = cnx.get_test_results()
    if failed_tests:
        logger.error("Some tests failed: {}".format(failed_tests.keys()))
        if options.allow_failures:
            logger.warning("Some tests failed but --allow-failures was set")
        else:
            RET_CODE = 1
    else:
        logger.info("All tests passed")

    if options.coverage:
        logger.info("Total coverage: {}%".format(cnx.total_coverage))

    sys.exit(RET_CODE)
