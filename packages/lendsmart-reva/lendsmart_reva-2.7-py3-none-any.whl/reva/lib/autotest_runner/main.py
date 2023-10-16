"""
    This module runns the test
"""
from ramda import path_or
import uuid
from abc import ABC, abstractmethod
from reva.exception import UnsupportedPlatformError
from autotest.lib.client_builder.aws.lambda_obj import LambdaObj
from reva.lib.utils.get_json_files import JsonFileGetter
from reva.lib.client.aws import S3Handler
from autotest.lib.runner.initializer import AutoTestInitializer
from autotest.lib.lib.lend_event import LendEvent
from autotest.lib.client_builder.aws.lambda_obj import LambdaObj
from autotest.lib.base.setup import DriverSetup

class RunnerInitializer:
    """
    This class handles the auto test
    """

    def __init__(self, arguments):
        self.arguments = arguments

    def start(self):
        """
        start the auto test process
        """
        if self.arguments.platform == "remote":
            return RemoteAutoTest(arguments=self.arguments).run()
        if self.arguments.platform == "local":
            return LocalAutoTest(arguments=self.arguments).run()
        raise UnsupportedPlatformError(
            "Unsupported platform " + self.arguments.platform
        )


class AutoTestRunner(ABC):
    """
    Autotest runner
    """

    def __init__(self, arguments):
        self.arguments = arguments

    def get_json(self):
        """
        This function will get the json
        """
        file_path = self.arguments.file_path
        file_location = self.arguments.file_location
        if file_location == "local":
            json_file = JsonFileGetter().get_file_by_path(file_path)
        if file_location == "s3":
            bucket = self.arguments.bucket
            json_file = S3Handler().get_json_from_s3(
                bucket=bucket, remote_file_path=file_location
            )
        return json_file

    def generate_payload(self)->list:
        """
        This function generate the data
        """
        result = []
        payload = self.get_json()
        for data in payload:
            data["test_data"]["combination_unique_id"] = str(uuid.uuid4())
            result.append(
                {
                    "event_data" : data
                }
            )
        return result

    @abstractmethod
    def run(self):
        """
        run the test
        """


class RemoteAutoTest(AutoTestRunner):
    """
    This will run the test on remote
    """

    def run(self):
        """
        Run the test in remote server
        """
        payload = self.generate_payload()
        for test_data in payload:
            print("Triggered-->", path_or("",["event_data","test_data","combination_unique_id"], test_data))
            LambdaObj().invoke(
                payload=test_data, function_name="autotest_test"
            )


class LocalAutoTest(AutoTestRunner):
    """
    This will run the test in local
    """

    def run(self):
        """
        Run in local
        """
        payload_list = self.generate_payload()
        for event_data in payload_list:
            test_data = path_or({},["event_data","test_data"], event_data)
            driver_path = path_or("",["chrome_driver_path"], test_data)
            chromium_path = path_or("",["headless_chromium_path"], test_data)
            browser_type = path_or("",["browser_type"], test_data)
            lend_event = LendEvent(event_data)
            driver = DriverSetup().get_driver(
                browser_type = browser_type or "headless-chromium",
                driver_path=driver_path,
                chromium_path=chromium_path
            )
            AutoTestInitializer(
                driver = driver,
                lend_event = lend_event
            ).initailize()
